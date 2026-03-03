#!/usr/bin/env python3
"""Quick diagnostic: test each data source independently before running the full pipeline."""

import asyncio
import sys
from datetime import date

# Ensure project root is on path
sys.path.insert(0, ".")


async def test_flights():
    from sources.flights.kiwi_client import search_flights

    print("=== Flights: LON → ATH, Aug 14 2026 ===")
    results = await search_flights("LON", "ATH", date(2026, 8, 14))
    print(f"  {len(results)} result(s)")
    for r in results[:3]:
        print(f"  • {r.airline:20s}  {r.price_currency} {r.price_amount:>6.0f}  {'(mock)' if r.notes and 'Mock' in r.notes else '(live)'}")
    print()


async def test_ferries():
    from sources.ferries.ferryhopper_scraper import search_ferries

    print("=== Ferries: PIR → MLO, Aug 14 2026 ===")
    results = await search_ferries("PIR", "MLO", date(2026, 8, 14))
    print(f"  {len(results)} result(s)")
    for r in results[:3]:
        label = r.operator or "Unknown"
        dur = f"{r.duration_minutes}min" if r.duration_minutes else "?"
        print(f"  • {label:20s}  EUR {r.price_amount:>6.1f}  {dur}")
    print()


async def test_accommodation():
    from sources.accommodation.booking_client import search_accommodation

    print("=== Accommodation: Milos, Aug 14–19 2026 ===")
    results = await search_accommodation("Milos", date(2026, 8, 14), date(2026, 8, 19))
    print(f"  {len(results)} result(s)")
    for r in results[:3]:
        src = f"[{r.source}]" if r.source else ""
        print(f"  • {r.name:30s}  {r.price_currency} {r.price_per_night:>6.0f}/night  rating {r.rating}  {src}")
    print()


async def main():
    print("TripForge — Live Source Diagnostics\n")

    await test_flights()
    await test_ferries()
    await test_accommodation()

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
