"""Ferryhopper scraper using Playwright for live ferry schedules."""

from __future__ import annotations

import asyncio
from datetime import date
from typing import Any

from config import CACHE_TTL_FERRIES, RATE_LIMIT_FERRYHOPPER
from models.trip import FerryOption
from research.cache import cached_get, cached_set
from research.rate_limit import get_limiter
from sources.ferries.static_routes import search_static_routes

_limiter = get_limiter("ferryhopper", RATE_LIMIT_FERRYHOPPER)

# Port name mappings for Ferryhopper URLs
PORT_NAMES = {
    "PIR": "piraeus",
    "MLO": "milos",
    "KOF": "koufonisia",
    "NAX": "naxos",
    "PAR": "paros",
    "SAN": "santorini",
    "MYK": "mykonos",
    "IOS": "ios",
    "SIF": "sifnos",
    "SER": "serifos",
    "FOL": "folegandros",
    "AMO": "amorgos",
    "RAF": "rafina",
}


async def search_ferries(
    origin_port: str,
    destination_port: str,
    travel_date: date,
    passengers: int = 1,
) -> list[FerryOption]:
    """Search for ferry options. Tries Playwright scraping, falls back to static DB.

    Args:
        origin_port: Port code (e.g. "PIR", "MLO")
        destination_port: Port code (e.g. "MLO", "KOF")
        travel_date: Date of travel
        passengers: Number of passengers
    """
    cache_params = dict(
        origin=origin_port, dest=destination_port,
        date=str(travel_date), pax=passengers,
    )
    cached = cached_get("ferries", CACHE_TTL_FERRIES, **cache_params)
    if cached is not None:
        return [FerryOption(**f) for f in cached]

    # Try Playwright scraping
    results = await _scrape_ferryhopper(origin_port, destination_port, travel_date, passengers)

    # Fall back to static routes if scraping fails or returns nothing
    if not results:
        results = search_static_routes(origin_port, destination_port, travel_date)

    if results:
        cached_set(
            "ferries",
            [f.model_dump() for f in results],
            CACHE_TTL_FERRIES,
            **cache_params,
        )

    return results


async def _scrape_ferryhopper(
    origin: str,
    destination: str,
    travel_date: date,
    passengers: int,
) -> list[FerryOption]:
    """Scrape Ferryhopper for real ferry schedules."""
    origin_name = PORT_NAMES.get(origin, origin.lower())
    dest_name = PORT_NAMES.get(destination, destination.lower())

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return []

    await _limiter.acquire()

    results: list[FerryOption] = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            url = (
                f"https://www.ferryhopper.com/en/ferry-routes/"
                f"{origin_name}-{dest_name}"
                f"?date={travel_date.isoformat()}&passengers={passengers}"
            )

            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(3000)

            # Look for ferry result cards
            cards = await page.query_selector_all('[data-testid="trip-card"], .trip-card, .ferry-result')

            for card in cards[:8]:
                text = await card.inner_text()
                lines = [l.strip() for l in text.split("\n") if l.strip()]

                option = _parse_ferry_card(origin, destination, lines)
                if option:
                    results.append(option)

            await browser.close()

    except Exception:
        # Scraping failed — caller will fall back to static routes
        pass

    return results


def _parse_ferry_card(origin: str, destination: str, lines: list[str]) -> FerryOption | None:
    """Best-effort parsing of a Ferryhopper result card text."""
    if len(lines) < 2:
        return None

    operator = ""
    price = 0.0
    duration = 0

    for line in lines:
        lower = line.lower()
        if any(op in lower for op in ["seajets", "blue star", "zante", "aegean speed", "minoan", "hellenic"]):
            operator = line.strip()
        if "€" in line or "eur" in lower:
            import re
            match = re.search(r"(\d+(?:\.\d{2})?)", line.replace(",", "."))
            if match:
                price = float(match.group(1))
        if "h" in lower and "m" in lower:
            import re
            h_match = re.search(r"(\d+)\s*h", lower)
            m_match = re.search(r"(\d+)\s*m", lower)
            hours = int(h_match.group(1)) if h_match else 0
            mins = int(m_match.group(1)) if m_match else 0
            duration = hours * 60 + mins

    return FerryOption(
        origin_port=origin,
        destination_port=destination,
        operator=operator or "Unknown",
        price_amount=price,
        price_currency="EUR",
        duration_minutes=duration,
        booking_url=f"https://www.ferryhopper.com/en/ferry-routes/{PORT_NAMES.get(origin, origin.lower())}-{PORT_NAMES.get(destination, destination.lower())}",
        is_high_speed=duration > 0 and duration < 300,
    )


def generate_ferryhopper_link(origin: str, destination: str, travel_date: date) -> str:
    """Generate a deep link to Ferryhopper search results."""
    origin_name = PORT_NAMES.get(origin, origin.lower())
    dest_name = PORT_NAMES.get(destination, destination.lower())
    return (
        f"https://www.ferryhopper.com/en/ferry-routes/"
        f"{origin_name}-{dest_name}?date={travel_date.isoformat()}"
    )
