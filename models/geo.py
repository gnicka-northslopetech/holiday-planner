"""Geographic data: airport codes, port codes, island info for Greek Islands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).parent.parent / "data"


class AirportCode(BaseModel):
    code: str
    name: str
    city: str
    country: str = "GR"


class PortCode(BaseModel):
    code: str
    name: str
    island: str
    notes: str = ""


class IslandInfo(BaseModel):
    name: str
    airport_code: str = ""
    port_code: str = ""
    port_name: str = ""
    needs_car: bool = False
    description: str = ""


# ── Lookup helpers ──

_airports: dict[str, AirportCode] | None = None
_ports: dict[str, PortCode] | None = None
_islands: dict[str, IslandInfo] | None = None


def load_airports() -> dict[str, AirportCode]:
    global _airports
    if _airports is None:
        path = DATA_DIR / "airport_codes.json"
        raw = json.loads(path.read_text())
        _airports = {k: AirportCode(**v) for k, v in raw.items()}
    return _airports


def load_ports() -> dict[str, PortCode]:
    global _ports
    if _ports is None:
        path = DATA_DIR / "port_codes.json"
        raw = json.loads(path.read_text())
        _ports = {k: PortCode(**v) for k, v in raw.items()}
    return _ports


def load_islands() -> dict[str, IslandInfo]:
    global _islands
    if _islands is None:
        path = DATA_DIR / "island_info.json"
        raw = json.loads(path.read_text())
        _islands = {k: IslandInfo(**v) for k, v in raw.items()}
    return _islands


def resolve_island(name: str) -> Optional[IslandInfo]:
    """Fuzzy-match an island name to our database."""
    islands = load_islands()
    # Exact match
    if name in islands:
        return islands[name]
    # Case-insensitive
    lower = name.lower()
    for key, info in islands.items():
        if key.lower() == lower:
            return info
    return None


def airport_for_city(city: str) -> str:
    """Return the primary airport IATA code for a city."""
    airports = load_airports()
    for code, airport in airports.items():
        if airport.city.lower() == city.lower():
            return code
    # Common city-to-airport mappings
    city_map = {
        "london": "LON",
        "athens": "ATH",
        "paris": "CDG",
        "berlin": "BER",
        "rome": "FCO",
        "amsterdam": "AMS",
    }
    return city_map.get(city.lower(), "")
