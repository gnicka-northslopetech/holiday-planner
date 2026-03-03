"""Accommodation search via SerpAPI Google Hotels (primary), with mock fallback."""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

import httpx

from config import CACHE_TTL_ACCOMMODATION, RATE_LIMIT_BOOKING, SERPAPI_KEY
from models.trip import AccommodationOption
from research.cache import cached_get, cached_set
from research.rate_limit import get_limiter

_limiter = get_limiter("booking", RATE_LIMIT_BOOKING)
_log = logging.getLogger(__name__)

SERPAPI_BASE = "https://serpapi.com/search"


async def search_accommodation(
    island: str,
    checkin: date,
    checkout: date,
    guests: int = 2,
    max_results: int = 6,
) -> list[AccommodationOption]:
    """Search for accommodation on a Greek island.

    Tries SerpAPI Google Hotels first, falls back to mock data.
    """
    cache_params = dict(
        island=island, checkin=str(checkin),
        checkout=str(checkout), guests=guests,
    )
    cached = cached_get("accommodation", CACHE_TTL_ACCOMMODATION, **cache_params)
    if cached is not None:
        return [AccommodationOption(**a) for a in cached]

    results: list[AccommodationOption] = []

    if SERPAPI_KEY:
        results = await _search_google_hotels(island, checkin, checkout, guests, max_results)

    if not results:
        _log.info("SerpAPI unavailable or returned no results for %s, using mock data", island)
        results = _mock_accommodation(island, checkin, checkout, guests)

    if results:
        cached_set(
            "accommodation",
            [a.model_dump() for a in results],
            CACHE_TTL_ACCOMMODATION,
            **cache_params,
        )

    return results


async def _search_google_hotels(
    island: str,
    checkin: date,
    checkout: date,
    guests: int,
    max_results: int,
) -> list[AccommodationOption]:
    """Search via SerpAPI's Google Hotels engine."""
    await _limiter.acquire()

    nights = (checkout - checkin).days

    params: dict[str, Any] = {
        "engine": "google_hotels",
        "q": f"{island} Greece",
        "check_in_date": checkin.isoformat(),
        "check_out_date": checkout.isoformat(),
        "adults": guests,
        "currency": "EUR",
        "api_key": SERPAPI_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(SERPAPI_BASE, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        _log.warning("SerpAPI Google Hotels request failed: %s", exc)
        return []

    results: list[AccommodationOption] = []

    for prop in data.get("properties", [])[:max_results]:
        total_rate = prop.get("total_rate", {})
        rate_per_night = prop.get("rate_per_night", {})

        total_price = float(total_rate.get("extracted_lowest", 0))
        price_per_night = float(rate_per_night.get("extracted_lowest", 0))

        # Derive price_per_night from total if not directly available
        if not price_per_night and total_price and nights > 0:
            price_per_night = round(total_price / nights, 0)

        # Google uses a 5-star rating scale; normalize to 10 for consistency
        raw_rating = prop.get("overall_rating", 0)
        rating = round(raw_rating * 2, 1)  # 4.5 → 9.0

        option = AccommodationOption(
            name=prop.get("name", "Unknown"),
            location=prop.get("description", ""),
            island=island,
            source="google_hotels",
            price_per_night=price_per_night,
            price_currency="EUR",
            total_price=total_price,
            rating=rating,
            rating_max=10.0,
            num_reviews=prop.get("reviews", 0),
            features=prop.get("amenities", [])[:5],
            booking_url=prop.get("link", ""),
        )
        results.append(option)

    return results


def _mock_accommodation(
    island: str,
    checkin: date,
    checkout: date,
    guests: int,
) -> list[AccommodationOption]:
    """Return mock accommodation data for development."""
    nights = (checkout - checkin).days

    mock_db: dict[str, list[dict[str, Any]]] = {
        "Milos": [
            {
                "name": "Echinousa Apartment no6",
                "location": "Psathi",
                "price": 118,
                "rating": 10.0,
                "features": ["1 bed", "sea view", "free daily cleaning", "port transfer"],
                "url": "https://www.holidu.com/d/62182229",
                "source": "holidu",
            },
            {
                "name": "Echinousa Katoikia no2",
                "location": "Psathi",
                "price": 118,
                "rating": 9.0,
                "features": ["1 bed", "king bed", "mountain views"],
                "url": "https://www.holidu.com/d/62175009",
                "source": "holidu",
            },
            {
                "name": "Nikos Family Milos",
                "location": "Adamas (port town)",
                "price": 177,
                "rating": 7.2,
                "features": ["2 bed", "sea view", "private terrace"],
                "url": "https://www.holidu.com/d/53364856",
                "source": "holidu",
            },
            {
                "name": "Echinousa Maisonette no4",
                "location": "Psathi",
                "price": 259,
                "rating": 10.0,
                "features": ["1 bed + living room", "3 balconies", "free port transfer"],
                "url": "https://www.holidu.com/d/62175042",
                "source": "holidu",
            },
            {
                "name": "Moon Kiss Apartment",
                "location": "Milos",
                "price": 321,
                "rating": 8.7,
                "features": ["sea view", "shared heated pool", "beachfront"],
                "url": "https://www.holidu.com/d/56256054",
                "source": "holidu",
            },
        ],
        "Koufonisia": [
            {
                "name": "Alkionides Studios",
                "location": "Chora · 600m from beach",
                "price": 85,
                "rating": 9.7,
                "reviews": 234,
                "features": [],
                "url": "https://www.booking.com/hotel/gr/alkionides-studios-koufonisi.html",
                "source": "booking.com",
            },
            {
                "name": "Aeolos Hotel",
                "location": "Chora · pool · 200m from port",
                "price": 114,
                "rating": 9.3,
                "features": ["breakfast buffet"],
                "url": "https://aeoloshotel.com",
                "source": "direct",
            },
            {
                "name": "Myrto Hotel",
                "location": "Chora · beachfront · 40m from beach · 200m from port",
                "price": 129,
                "rating": 8.8,
                "reviews": 385,
                "features": [],
                "url": "https://www.myrtohotelkoufonisia.com",
                "source": "direct",
            },
            {
                "name": "Keros Art Hotel",
                "location": "Chora · boutique · pool · sea-view balconies",
                "price": 194,
                "rating": 9.7,
                "reviews": 707,
                "features": ["daily breakfast"],
                "url": "https://www.booking.com/hotel/gr/keros-art.html",
                "source": "booking.com",
            },
            {
                "name": "Thalasso-Koufonisia",
                "location": "Airbnb · traditional island house · 3 guests",
                "price": 139,
                "rating": 4.96,
                "rating_max": 5.0,
                "reviews": 53,
                "features": [],
                "url": "https://www.airbnb.com/rooms/3624609",
                "source": "airbnb",
            },
            {
                "name": "ARCHANGELO Sea View",
                "location": "Airbnb · Cycladic apartment · 400m from port beach",
                "price": 164,
                "rating": 4.98,
                "rating_max": 5.0,
                "reviews": 45,
                "features": [],
                "url": "https://www.airbnb.com/rooms/50684416",
                "source": "airbnb",
            },
        ],
    }

    listings = mock_db.get(island, [
        {
            "name": f"{island} Studio",
            "location": f"{island} Town",
            "price": 100,
            "rating": 8.0,
            "features": [],
            "url": f"https://www.booking.com/searchresults.html?ss={island}",
            "source": "booking.com",
        },
    ])

    return [
        AccommodationOption(
            name=l["name"],
            location=l["location"],
            island=island,
            source=l.get("source", "booking.com"),
            price_per_night=l["price"],
            price_currency="USD",
            total_price=l["price"] * nights,
            rating=l["rating"],
            rating_max=l.get("rating_max", 10.0),
            num_reviews=l.get("reviews", 0),
            features=l.get("features", []),
            booking_url=l["url"],
        )
        for l in listings
    ]
