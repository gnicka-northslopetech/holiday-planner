"""Airbnb deep link generator — no API, just search URL construction."""

from __future__ import annotations

from datetime import date
from urllib.parse import quote


def airbnb_search_url(
    island: str,
    checkin: date,
    checkout: date,
    adults: int = 2,
    country: str = "Greece",
) -> str:
    """Generate an Airbnb search URL for a Greek island."""
    location = quote(f"{island}, {country}")
    return (
        f"https://www.airbnb.com/s/{location}/homes"
        f"?checkin={checkin.isoformat()}"
        f"&checkout={checkout.isoformat()}"
        f"&adults={adults}"
    )


def booking_search_url(
    island: str,
    checkin: date,
    checkout: date,
    adults: int = 2,
) -> str:
    """Generate a Booking.com search URL."""
    return (
        f"https://www.booking.com/searchresults.html"
        f"?ss={quote(island)}"
        f"&checkin={checkin.isoformat()}"
        f"&checkout={checkout.isoformat()}"
        f"&group_adults={adults}"
    )


def holidu_search_url(
    island: str,
    checkin: date,
    checkout: date,
    adults: int = 2,
    country: str = "greece",
) -> str:
    """Generate a Holidu search URL."""
    return (
        f"https://www.holidu.com/vacation-rentals/{country}/{island.lower()}"
        f"?checkin={checkin.isoformat()}"
        f"&checkout={checkout.isoformat()}"
        f"&adults={adults}"
    )
