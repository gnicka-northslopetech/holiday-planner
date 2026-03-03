"""Flight search via SerpAPI Google Flights (primary) or Kiwi Tequila (secondary).

Falls back to mock data if neither API key is configured or calls fail.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

import httpx

from config import (
    CACHE_TTL_FLIGHTS,
    KIWI_API_KEY,
    RATE_LIMIT_KIWI,
    SERPAPI_KEY,
)
from models.trip import FlightOption
from research.cache import cached_get, cached_set
from research.rate_limit import get_limiter

TEQUILA_BASE = "https://api.tequila.kiwi.com"
SERPAPI_BASE = "https://serpapi.com/search"

# Google Flights needs real airport codes, not Kiwi-style city codes
_CITY_TO_AIRPORT = {
    "LON": "LHR",
    "NYC": "JFK",
    "PAR": "CDG",
    "BER": "BER",
    "ROM": "FCO",
    "MIL": "MXP",
}

_limiter = get_limiter("kiwi", RATE_LIMIT_KIWI)
_log = logging.getLogger(__name__)


async def search_flights(
    origin: str,
    destination: str,
    date_from: date,
    date_to: date | None = None,
    return_from: date | None = None,
    return_to: date | None = None,
    adults: int = 1,
    max_results: int = 5,
    currency: str = "EUR",
) -> list[FlightOption]:
    """Search for flights. Tries SerpAPI → Kiwi → mock.

    Args:
        origin: IATA code (e.g. "LON", "ATH")
        destination: IATA code (e.g. "ATH", "MLO")
        date_from: Earliest departure date
        date_to: Latest departure date (defaults to date_from)
        return_from: Earliest return date (omit for one-way)
        return_to: Latest return date
        adults: Number of passengers
        max_results: Max flight options to return
        currency: Price currency
    """
    date_to = date_to or date_from

    # Check cache
    cache_params = dict(
        origin=origin, dest=destination,
        date_from=str(date_from), date_to=str(date_to),
        adults=adults,
    )
    cached = cached_get("kiwi_flights", CACHE_TTL_FLIGHTS, **cache_params)
    if cached is not None:
        return [FlightOption(**f) for f in cached]

    results: list[FlightOption] = []

    # Try SerpAPI Google Flights first
    if SERPAPI_KEY:
        results = await _search_serpapi(
            origin, destination, date_from, return_from,
            adults, max_results, currency,
        )

    # Try Kiwi Tequila as secondary
    if not results and KIWI_API_KEY:
        results = await _search_kiwi(
            origin, destination, date_from, date_to,
            return_from, return_to, adults, max_results, currency,
        )

    # Fall back to mock
    if not results:
        _log.info("No API keys or all APIs failed — using mock flights")
        return _mock_flights(origin, destination, date_from, adults)

    # Cache real results
    cached_set(
        "kiwi_flights",
        [f.model_dump() for f in results],
        CACHE_TTL_FLIGHTS,
        **cache_params,
    )

    return results


# ── SerpAPI Google Flights ──────────────────────────────────────────────


async def _search_serpapi(
    origin: str,
    destination: str,
    outbound_date: date,
    return_date: date | None,
    adults: int,
    max_results: int,
    currency: str,
) -> list[FlightOption]:
    """Search via SerpAPI's Google Flights engine."""
    await _limiter.acquire()

    dep_id = _CITY_TO_AIRPORT.get(origin, origin)
    arr_id = _CITY_TO_AIRPORT.get(destination, destination)

    params: dict[str, Any] = {
        "engine": "google_flights",
        "departure_id": dep_id,
        "arrival_id": arr_id,
        "outbound_date": outbound_date.isoformat(),
        "adults": adults,
        "currency": currency,
        "type": "2" if not return_date else "1",  # 2 = one-way, 1 = round trip
        "api_key": SERPAPI_KEY,
    }
    if return_date:
        params["return_date"] = return_date.isoformat()

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(SERPAPI_BASE, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        _log.warning("SerpAPI request failed: %s", exc)
        return []

    results: list[FlightOption] = []

    for group in (data.get("best_flights", []) + data.get("other_flights", [])):
        if len(results) >= max_results:
            break

        flights = group.get("flights", [])
        if not flights:
            continue

        first_leg = flights[0]
        dep_airport = first_leg.get("departure_airport", {})
        arr_airport = flights[-1].get("arrival_airport", {})

        option = FlightOption(
            origin=dep_airport.get("id", origin),
            destination=arr_airport.get("id", destination),
            airline=first_leg.get("airline", ""),
            flight_number=first_leg.get("flight_number", ""),
            price_amount=group.get("price", 0),
            price_currency=currency,
            duration_minutes=group.get("total_duration", 0),
            booking_url=data.get("search_metadata", {}).get("google_flights_url", ""),
            is_direct=len(flights) == 1,
        )
        results.append(option)

    return results


# ── Kiwi Tequila (secondary) ───────────────────────────────────────────


async def _search_kiwi(
    origin: str,
    destination: str,
    date_from: date,
    date_to: date,
    return_from: date | None,
    return_to: date | None,
    adults: int,
    max_results: int,
    currency: str,
) -> list[FlightOption]:
    """Search via Kiwi.com Tequila API."""
    await _limiter.acquire()

    params: dict[str, Any] = {
        "fly_from": origin,
        "fly_to": destination,
        "date_from": date_from.strftime("%d/%m/%Y"),
        "date_to": date_to.strftime("%d/%m/%Y"),
        "adults": adults,
        "curr": currency,
        "limit": max_results,
        "sort": "price",
        "one_for_city": 0,
        "max_stopovers": 0,
    }

    if return_from:
        params["return_from"] = return_from.strftime("%d/%m/%Y")
        params["return_to"] = (return_to or return_from).strftime("%d/%m/%Y")
        params["flight_type"] = "round"
    else:
        params["flight_type"] = "oneway"

    headers = {"apikey": KIWI_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{TEQUILA_BASE}/v2/search",
                params=params,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        _log.warning("Kiwi API request failed: %s", exc)
        return []

    results = []
    for item in data.get("data", [])[:max_results]:
        route = item.get("route", [{}])[0] if item.get("route") else {}
        option = FlightOption(
            origin=origin,
            destination=destination,
            airline=route.get("airline", ""),
            flight_number=route.get("flight_no", ""),
            price_amount=item.get("price", 0),
            price_currency=currency,
            duration_minutes=item.get("duration", {}).get("total", 0) // 60,
            booking_url=item.get("deep_link", ""),
            is_direct=item.get("max_stopovers", 0) == 0,
        )
        results.append(option)

    return results


# ── Mock fallback ───────────────────────────────────────────────────────


def _mock_flights(
    origin: str, destination: str, depart: date, adults: int
) -> list[FlightOption]:
    """Return mock flight data when no API key is configured."""
    mock_data: dict[tuple[str, str], list[dict[str, Any]]] = {
        ("LON", "ATH"): [
            {"airline": "British Airways", "price": 130, "cur": "GBP", "dur": 210},
            {"airline": "Aegean Airlines", "price": 145, "cur": "GBP", "dur": 210},
            {"airline": "easyJet", "price": 95, "cur": "GBP", "dur": 215},
            {"airline": "Ryanair", "price": 89, "cur": "GBP", "dur": 220},
            {"airline": "Wizz Air", "price": 85, "cur": "GBP", "dur": 225},
        ],
        ("ATH", "LON"): [
            {"airline": "Ryanair", "price": 79, "cur": "GBP", "dur": 220},
            {"airline": "Aegean Airlines", "price": 135, "cur": "GBP", "dur": 210},
            {"airline": "easyJet", "price": 95, "cur": "GBP", "dur": 215},
        ],
        ("ATH", "MLO"): [
            {"airline": "Olympic Air", "price": 55, "cur": "EUR", "dur": 40},
            {"airline": "Sky Express", "price": 45, "cur": "EUR", "dur": 40},
        ],
        ("MLO", "ATH"): [
            {"airline": "Olympic Air", "price": 60, "cur": "EUR", "dur": 40},
            {"airline": "Sky Express", "price": 50, "cur": "EUR", "dur": 40},
        ],
    }

    key = (origin, destination)
    flights = mock_data.get(key, [
        {"airline": "Unknown Airline", "price": 100, "cur": "EUR", "dur": 120},
    ])

    return [
        FlightOption(
            origin=origin,
            destination=destination,
            airline=f["airline"],
            price_amount=f["price"],
            price_currency=f["cur"],
            duration_minutes=f["dur"],
            is_direct=True,
            notes=f"Mock data — {depart.strftime('%b %d')}",
        )
        for f in flights
    ]
