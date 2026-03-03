"""Tests for data source clients (using mock data)."""

import asyncio
from datetime import date

from sources.flights.kiwi_client import search_flights
from sources.ferries.static_routes import search_static_routes
from sources.accommodation.booking_client import search_accommodation
from sources.accommodation.airbnb_links import airbnb_search_url, booking_search_url


def test_mock_flights():
    """Test flight search returns mock data when no API key."""
    results = asyncio.run(search_flights(
        origin="LON",
        destination="ATH",
        date_from=date(2026, 8, 14),
        adults=2,
    ))
    assert len(results) > 0
    assert results[0].origin == "LON"
    assert results[0].destination == "ATH"
    assert results[0].price_amount > 0


def test_mock_flights_ath_mlo():
    results = asyncio.run(search_flights(
        origin="ATH",
        destination="MLO",
        date_from=date(2026, 8, 14),
    ))
    assert len(results) > 0
    assert any("Olympic" in f.airline for f in results)


def test_static_ferry_routes():
    results = search_static_routes("PIR", "MLO", date(2026, 8, 14))
    assert len(results) > 0
    assert any(f.is_high_speed for f in results)
    assert results[0].origin_port == "PIR"


def test_static_ferry_milos_koufonisia():
    results = search_static_routes("MLO", "KOF", date(2026, 8, 19))
    assert len(results) > 0
    assert any("SeaJets" in f.operator for f in results)


def test_static_ferry_koufonisia_piraeus():
    results = search_static_routes("KOF", "PIR", date(2026, 8, 21))
    assert len(results) > 0


def test_mock_accommodation_milos():
    results = asyncio.run(search_accommodation(
        island="Milos",
        checkin=date(2026, 8, 14),
        checkout=date(2026, 8, 19),
    ))
    assert len(results) > 0
    assert results[0].island == "Milos"
    assert results[0].price_per_night > 0


def test_mock_accommodation_koufonisia():
    results = asyncio.run(search_accommodation(
        island="Koufonisia",
        checkin=date(2026, 8, 19),
        checkout=date(2026, 8, 21),
    ))
    assert len(results) > 0
    assert any("Alkionides" in a.name for a in results)


def test_airbnb_link():
    url = airbnb_search_url("Koufonisia", date(2026, 8, 19), date(2026, 8, 21))
    assert "airbnb.com" in url
    assert "2026-08-19" in url


def test_booking_link():
    url = booking_search_url("Milos", date(2026, 8, 14), date(2026, 8, 19))
    assert "booking.com" in url
    assert "Milos" in url
