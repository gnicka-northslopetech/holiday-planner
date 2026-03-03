"""Tests for core Pydantic models."""

from datetime import date

from models.trip import (
    TripSpecification,
    TripOrigin,
    IslandStop,
    FlightOption,
    FerryOption,
    AccommodationOption,
    TransportLeg,
    TransportMode,
    DayPlan,
    Itinerary,
    AccommodationSection,
)
from models.geo import resolve_island, airport_for_city


def test_trip_spec_from_yaml():
    """Test creating a TripSpecification from YAML-like data."""
    spec = TripSpecification(
        title="Greece 2026",
        origins=[
            TripOrigin(city="London", country="GB", airport_code="LON", num_travelers=4, label="London crew"),
            TripOrigin(city="Athens", country="GR", airport_code="ATH", num_travelers=2, label="Athens crew"),
        ],
        hub_city="Athens",
        hub_airport="ATH",
        stops=[
            IslandStop(island="Milos", nights=5, port_code="MLO", airport_code="MLO", needs_car=True),
            IslandStop(island="Koufonisia", nights=2, port_code="KOF", needs_car=False),
        ],
        start_date=date(2026, 8, 14),
        end_date=date(2026, 8, 21),
        total_travelers=6,
        group_description="3 couples",
    )

    assert spec.title == "Greece 2026"
    assert len(spec.origins) == 2
    assert len(spec.stops) == 2
    assert spec.stops[0].island == "Milos"
    assert spec.stops[1].needs_car is False
    assert (spec.end_date - spec.start_date).days == 7


def test_flight_option():
    f = FlightOption(
        origin="LON",
        destination="ATH",
        airline="easyJet",
        price_amount=95,
        price_currency="GBP",
        duration_minutes=215,
    )
    assert f.is_direct is True
    assert f.price_amount == 95


def test_ferry_option():
    f = FerryOption(
        origin_port="MLO",
        destination_port="KOF",
        operator="SeaJets",
        price_amount=107.70,
        duration_minutes=240,
        is_high_speed=True,
    )
    assert f.is_high_speed is True


def test_transport_leg_badge():
    leg = TransportLeg(
        mode=TransportMode.FLIGHT,
        origin="London",
        destination="Athens",
    )
    assert leg.badge_class == "badge-flight"

    ferry_leg = TransportLeg(
        mode=TransportMode.FERRY,
        origin="Milos",
        destination="Koufonisia",
    )
    assert ferry_leg.badge_class == "badge-ferry"


def test_resolve_island():
    info = resolve_island("Milos")
    assert info is not None
    assert info.airport_code == "MLO"
    assert info.needs_car is True

    info2 = resolve_island("Koufonisia")
    assert info2 is not None
    assert info2.airport_code == ""
    assert info2.needs_car is False

    assert resolve_island("Atlantis") is None


def test_resolve_island_case_insensitive():
    info = resolve_island("milos")
    assert info is not None
    assert info.name == "Milos"


def test_airport_for_city():
    assert airport_for_city("London") == "LON"
    assert airport_for_city("Athens") == "ATH"


def test_accommodation_option():
    a = AccommodationOption(
        name="Test Hotel",
        island="Milos",
        price_per_night=118,
        total_price=590,
        rating=9.5,
        rating_max=10.0,
    )
    assert a.total_price == 590


def test_itinerary_construction():
    it = Itinerary(
        title="Test Trip",
        subtitle="Milos & Koufonisia",
        date_range="Aug 14 – Aug 21",
        days=[
            DayPlan(date_label="Aug 14", title="Travel Day"),
        ],
        accommodation_sections=[
            AccommodationSection(
                title="Milos Accommodation",
                options=[
                    AccommodationOption(name="Test", island="Milos"),
                ],
            ),
        ],
    )
    assert len(it.days) == 1
    assert len(it.accommodation_sections) == 1
