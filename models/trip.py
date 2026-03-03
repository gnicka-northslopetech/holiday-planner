"""Core Pydantic models: TripSpecification → Itinerary pipeline."""

from __future__ import annotations

from datetime import date, time, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Input Models ──


class TransportMode(str, Enum):
    FLIGHT = "flight"
    FERRY = "ferry"
    TAXI = "taxi"
    BUS = "bus"
    WALK = "walk"


class TripOrigin(BaseModel):
    """One origin city for a subgroup of travelers."""

    city: str = Field(description="City name, e.g. 'London'")
    country: str = Field(default="", description="Country code, e.g. 'GB'")
    airport_code: str = Field(default="", description="IATA code, e.g. 'LON'")
    num_travelers: int = Field(default=2, ge=1)
    label: str = Field(default="", description="Group label, e.g. 'London crew'")


class IslandStop(BaseModel):
    """A stop on the island-hopping itinerary."""

    island: str = Field(description="Island name, e.g. 'Milos'")
    nights: int = Field(ge=1)
    port_code: str = Field(default="")
    airport_code: str = Field(default="")
    needs_car: bool = Field(default=False)
    notes: str = Field(default="")


class TripPreferences(BaseModel):
    """Structured user preferences gathered via conversational flow."""

    vibes: list[str] = Field(default_factory=list)
    vibe_notes: str = ""
    budget_level: str = "mid_range"
    max_per_night_eur: float | None = None
    accommodation_styles: list[str] = Field(default_factory=list)
    transport_preference: str = "no_preference"
    activities: list[str] = Field(default_factory=list)
    must_do: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    dietary_requirements: list[str] = Field(default_factory=list)
    accessibility_needs: str = ""
    date_flexibility: str = "fixed"
    group_dynamics_notes: str = ""
    raw_answers: list[dict] = Field(default_factory=list)


class TripSpecification(BaseModel):
    """Structured trip brief — parsed from user's free-text input."""

    title: str = Field(default="Greek Islands Trip")
    origins: list[TripOrigin] = Field(min_length=1)
    hub_city: str = Field(
        default="Athens",
        description="Mainland hub for connecting to islands",
    )
    hub_airport: str = Field(default="ATH")
    stops: list[IslandStop] = Field(min_length=1)
    start_date: date
    end_date: date
    total_travelers: int = Field(ge=1)
    group_description: str = Field(default="")
    budget_notes: str = Field(default="")
    preferences: list[str] = Field(default_factory=list)
    rich_preferences: TripPreferences | None = None


# ── Research Result Models ──


class FlightOption(BaseModel):
    """A single flight option from search results."""

    origin: str
    destination: str
    airline: str = ""
    flight_number: str = ""
    departure: Optional[datetime] = None
    arrival: Optional[datetime] = None
    duration_minutes: int = 0
    price_amount: float = 0.0
    price_currency: str = "EUR"
    booking_url: str = ""
    is_direct: bool = True
    notes: str = ""


class FerryOption(BaseModel):
    """A single ferry option from search results."""

    origin_port: str
    destination_port: str
    operator: str = ""
    vessel_name: str = ""
    departure_time: Optional[time] = None
    arrival_time: Optional[time] = None
    duration_minutes: int = 0
    price_amount: float = 0.0
    price_currency: str = "EUR"
    booking_url: str = ""
    sailing_days: list[str] = Field(
        default_factory=list,
        description="Days of week this route runs, e.g. ['Mon', 'Wed', 'Fri']",
    )
    notes: str = ""
    is_high_speed: bool = False


class AccommodationOption(BaseModel):
    """A single accommodation listing."""

    name: str
    location: str = ""
    island: str = ""
    source: str = Field(default="", description="booking.com, airbnb, holidu, etc.")
    price_per_night: float = 0.0
    price_currency: str = "USD"
    total_price: float = 0.0
    rating: float = 0.0
    rating_max: float = 10.0
    num_reviews: int = 0
    bedrooms: int = 1
    features: list[str] = Field(default_factory=list)
    booking_url: str = ""
    notes: str = ""


# ── Itinerary Output Models ──


class TransportLeg(BaseModel):
    """A single transport segment in the itinerary."""

    mode: TransportMode
    origin: str
    destination: str
    description: str = ""
    duration: str = ""
    price_display: str = ""
    options: list[FlightOption | FerryOption] = Field(default_factory=list)
    notes: str = ""
    badge_class: str = ""

    def model_post_init(self, __context: object) -> None:
        if not self.badge_class:
            badge_map = {
                TransportMode.FLIGHT: "badge-flight",
                TransportMode.FERRY: "badge-ferry",
                TransportMode.TAXI: "badge-taxi",
            }
            self.badge_class = badge_map.get(self.mode, "badge-taxi")


class DayPlan(BaseModel):
    """One day (or multi-day block) in the rendered itinerary."""

    date_label: str = Field(description="e.g. 'Thu Aug 14' or 'Aug 14–19'")
    title: str = Field(description="e.g. 'Travel Day' or 'Milos'")
    subtitle: str = Field(default="", description="e.g. 'London → Athens → Milos'")
    transport_legs: list[TransportLeg] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    is_highlight: bool = Field(
        default=False, description="Use amber accent instead of cyan"
    )
    nights: int = Field(default=0)
    needs_car: bool = Field(default=False)


class CostLineItem(BaseModel):
    """One row in the cost breakdown table."""

    label: str
    amount_display: str


class CostBreakdown(BaseModel):
    """Cost breakdown for a specific origin group."""

    origin_label: str = Field(description="e.g. 'London couple'")
    line_items: list[CostLineItem] = Field(default_factory=list)
    total_display: str = ""


class ActionItem(BaseModel):
    """An urgency-ordered booking action."""

    priority: int = Field(ge=1)
    title: str
    reason: str = ""
    links: list[tuple[str, str]] = Field(
        default_factory=list, description="List of (label, url) tuples"
    )


class UsefulLink(BaseModel):
    """A link card for the useful links grid."""

    category: str = Field(description="e.g. 'Flights', 'Ferries'")
    name: str = Field(description="e.g. 'Skyscanner'")
    url: str = ""


class Itinerary(BaseModel):
    """The complete rendered itinerary — input to Jinja2 template."""

    title: str = "Greek Islands Trip"
    subtitle: str = ""
    date_range: str = ""
    group_info: str = ""
    route_summary: list[str] = Field(
        default_factory=list,
        description="Route stops for visual map, e.g. ['London', 'Athens', 'Milos', 'Koufonisia']",
    )

    days: list[DayPlan] = Field(default_factory=list)

    accommodation_sections: list[AccommodationSection] = Field(default_factory=list)

    cost_breakdowns: list[CostBreakdown] = Field(default_factory=list)

    action_items: list[ActionItem] = Field(default_factory=list)

    useful_links: list[UsefulLink] = Field(default_factory=list)

    generated_at: str = ""
    notes: str = ""


class AccommodationSection(BaseModel):
    """A group of accommodation options for one island/stop."""

    title: str = Field(
        description="e.g. 'Milos Accommodation · Aug 14–19 (5 nights, 2 guests)'"
    )
    options: list[AccommodationOption] = Field(default_factory=list)


# Fix forward reference
Itinerary.model_rebuild()
