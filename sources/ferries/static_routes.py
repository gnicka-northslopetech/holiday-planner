"""Static ferry route database for Greek islands — fallback when scraping fails."""

from __future__ import annotations

import json
from datetime import date, time
from pathlib import Path

from models.trip import FerryOption

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def _load_routes() -> list[dict]:
    path = DATA_DIR / "ferry_routes.json"
    data = json.loads(path.read_text())
    return data.get("routes", [])


def search_static_routes(
    origin: str,
    destination: str,
    travel_date: date,
) -> list[FerryOption]:
    """Look up ferry routes from the static database."""
    routes = _load_routes()
    results: list[FerryOption] = []

    for route in routes:
        if route["origin"] == origin and route["destination"] == destination:
            # Add high-speed option
            if route.get("high_speed_duration_minutes"):
                price_range = route.get("high_speed_price_eur", [0, 0])
                low = price_range[0] if price_range else 0
                high = price_range[1] if len(price_range) > 1 else low

                for operator in route.get("operators", ["Unknown"])[:2]:
                    results.append(FerryOption(
                        origin_port=origin,
                        destination_port=destination,
                        operator=operator,
                        duration_minutes=route["high_speed_duration_minutes"],
                        price_amount=(low + high) / 2,
                        price_currency="EUR",
                        is_high_speed=True,
                        notes=route.get("notes", ""),
                        booking_url=_operator_url(operator),
                    ))

            # Add conventional option if available
            if route.get("conventional_duration_minutes"):
                price_range = route.get("conventional_price_eur", [0, 0])
                low = price_range[0] if price_range else 0
                high = price_range[1] if len(price_range) > 1 else low

                results.append(FerryOption(
                    origin_port=origin,
                    destination_port=destination,
                    operator=route.get("operators", ["Unknown"])[-1],
                    duration_minutes=route["conventional_duration_minutes"],
                    price_amount=(low + high) / 2,
                    price_currency="EUR",
                    is_high_speed=False,
                    notes=route.get("notes", ""),
                    booking_url=_operator_url(route.get("operators", ["Unknown"])[-1]),
                ))

    return results


def _operator_url(operator: str) -> str:
    urls = {
        "SeaJets": "https://www.seajets.com",
        "Blue Star Ferries": "https://www.bluestarferries.com",
        "Zante Ferries": "https://www.zanteferries.gr",
        "Aegean Speed Lines": "https://www.aegeanspeedlines.gr",
        "Minoan Lines": "https://www.minoan.gr",
        "Small Cyclades Lines": "https://www.ferryhopper.com",
        "Hellenic Seaways": "https://www.hellenicseaways.gr",
    }
    return urls.get(operator, "https://www.ferryhopper.com")
