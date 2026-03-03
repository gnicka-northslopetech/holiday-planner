"""Integration test: full pipeline from YAML → HTML (without API keys)."""

import asyncio
from datetime import date
from pathlib import Path

import yaml

from models.trip import TripSpecification
from agents.orchestrator import run_orchestrator
from output.renderer import render_itinerary


def test_full_pipeline():
    """Run the full pipeline with the Greece 2026 test case."""
    yaml_path = Path(__file__).parent.parent / "trips" / "greece-2026.yaml"
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    spec = TripSpecification(**data)
    assert spec.title == "Greece 2026"

    # Run orchestrator (will use mock data since no API key)
    itinerary = asyncio.run(run_orchestrator(spec))

    assert itinerary.title == "Greece 2026"
    assert len(itinerary.days) > 0
    assert len(itinerary.accommodation_sections) > 0
    assert len(itinerary.action_items) > 0

    # Check we have itinerary days for travel, island stays, transfers, and return
    day_titles = [d.title for d in itinerary.days]
    assert "Travel Day" in day_titles
    assert "Milos" in day_titles
    assert "Koufonisia" in day_titles
    assert "Return" in day_titles

    # Check accommodation sections exist for both islands
    acc_titles = [s.title for s in itinerary.accommodation_sections]
    assert any("Milos" in t for t in acc_titles)
    assert any("Koufonisia" in t for t in acc_titles)

    # Render to HTML
    output_path = Path(__file__).parent / "fixtures" / "test_output.html"
    html_path = render_itinerary(itinerary, output_path)

    assert html_path.exists()
    html = html_path.read_text()
    assert "Greece 2026" in html
    assert "Milos" in html
    assert "Koufonisia" in html
    assert "TripForge" in html

    # Cleanup
    html_path.unlink(missing_ok=True)
