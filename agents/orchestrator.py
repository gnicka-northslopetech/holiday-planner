"""Claude tool-use orchestrator — the brain of TripForge."""

from __future__ import annotations

import asyncio
import json
from datetime import date, timedelta
from typing import Any

import anthropic
from rich.console import Console

from agents.prompts import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    ITINERARY_SYNTHESIS_PROMPT,
    TRIP_EXTRACTION_PROMPT,
    PREFERENCE_QUESTION_PROMPT,
    PREFERENCE_EXTRACTION_PROMPT,
    PREFERENCE_SUMMARY_PROMPT,
)
from config import ANTHROPIC_API_KEY, ORCHESTRATOR_MODEL, EXTRACTION_MODEL
from models.trip import (
    TripSpecification,
    TripPreferences,
    Itinerary,
    FlightOption,
    FerryOption,
    AccommodationOption,
    DayPlan,
    TransportLeg,
    TransportMode,
    AccommodationSection,
    CostBreakdown,
    CostLineItem,
    ActionItem,
    UsefulLink,
)
from models.geo import resolve_island, load_ports
from sources.flights.kiwi_client import search_flights
from sources.ferries.ferryhopper_scraper import search_ferries
from sources.ferries.static_routes import search_static_routes
from sources.accommodation.booking_client import search_accommodation
from sources.accommodation.airbnb_links import airbnb_search_url, booking_search_url, holidu_search_url
from research.parallel import run_parallel_research

console = Console()


# ── Tool definitions for Claude ──

TOOLS = [
    {
        "name": "search_flights",
        "description": "Search for flight options between two airports",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Origin IATA code"},
                "destination": {"type": "string", "description": "Destination IATA code"},
                "date": {"type": "string", "description": "Travel date YYYY-MM-DD"},
                "adults": {"type": "integer", "description": "Number of passengers"},
            },
            "required": ["origin", "destination", "date"],
        },
    },
    {
        "name": "search_ferries",
        "description": "Search for ferry options between two ports",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin_port": {"type": "string", "description": "Origin port code"},
                "destination_port": {"type": "string", "description": "Destination port code"},
                "date": {"type": "string", "description": "Travel date YYYY-MM-DD"},
                "passengers": {"type": "integer", "description": "Number of passengers"},
            },
            "required": ["origin_port", "destination_port", "date"],
        },
    },
    {
        "name": "search_accommodation",
        "description": "Search for accommodation on a Greek island",
        "input_schema": {
            "type": "object",
            "properties": {
                "island": {"type": "string", "description": "Island name"},
                "checkin": {"type": "string", "description": "Check-in date YYYY-MM-DD"},
                "checkout": {"type": "string", "description": "Check-out date YYYY-MM-DD"},
                "guests": {"type": "integer", "description": "Number of guests"},
            },
            "required": ["island", "checkin", "checkout"],
        },
    },
    {
        "name": "get_island_info",
        "description": "Get details about a Greek island (ports, airports, car needs)",
        "input_schema": {
            "type": "object",
            "properties": {
                "island": {"type": "string", "description": "Island name"},
            },
            "required": ["island"],
        },
    },
]


async def extract_trip_spec(brief: str) -> TripSpecification:
    """Use Claude to extract structured trip details from free-text brief."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=EXTRACTION_MODEL,
        max_tokens=2000,
        system=TRIP_EXTRACTION_PROMPT,
        messages=[{"role": "user", "content": brief}],
    )

    text = response.content[0].text
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    data = json.loads(text)
    return TripSpecification(**data)


PREFERENCE_CATEGORIES = ["vibe", "budget", "activities", "practical"]


async def generate_preference_question(
    spec: TripSpecification,
    category: str,
    previous_answers: list[dict],
) -> dict[str, Any]:
    """Generate a single conversational preference question for the given category."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    trip_details = f"{spec.title}: {', '.join(s.island for s in spec.stops)}, " \
                   f"{spec.start_date} to {spec.end_date}, {spec.total_travelers} travelers"
    prev_str = json.dumps(previous_answers, indent=2) if previous_answers else "None yet"

    prompt = PREFERENCE_QUESTION_PROMPT.format(
        trip_details=trip_details,
        category=category,
        previous_answers=prev_str,
    )

    response = client.messages.create(
        model=EXTRACTION_MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


async def extract_structured_preferences(
    spec: TripSpecification,
    answers: list[dict],
) -> TripPreferences:
    """Extract structured TripPreferences from conversation Q&A pairs."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    trip_details = f"{spec.title}: {', '.join(s.island for s in spec.stops)}, " \
                   f"{spec.start_date} to {spec.end_date}, {spec.total_travelers} travelers"
    conv_str = json.dumps(answers, indent=2)

    prompt = PREFERENCE_EXTRACTION_PROMPT.format(
        trip_details=trip_details,
        conversation=conv_str,
    )

    response = client.messages.create(
        model=EXTRACTION_MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    data = json.loads(text)
    data["raw_answers"] = answers
    return TripPreferences(**data)


async def generate_preference_summary(
    spec: TripSpecification,
    prefs: TripPreferences,
) -> str:
    """Generate a friendly summary of preferences for user confirmation."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    trip_details = f"{spec.title}: {', '.join(s.island for s in spec.stops)}, " \
                   f"{spec.start_date} to {spec.end_date}, {spec.total_travelers} travelers"

    prompt = PREFERENCE_SUMMARY_PROMPT.format(
        trip_details=trip_details,
        preferences=prefs.model_dump_json(indent=2),
    )

    response = client.messages.create(
        model=EXTRACTION_MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text.strip()


async def run_orchestrator(spec: TripSpecification) -> Itinerary:
    """Run the full orchestration pipeline: research → synthesize → itinerary.

    This can run in two modes:
    1. With ANTHROPIC_API_KEY: Uses Claude tool-use loop for intelligent orchestration
    2. Without API key: Runs deterministic research pipeline directly
    """
    if ANTHROPIC_API_KEY:
        return await _run_with_claude(spec)
    else:
        return await _run_deterministic(spec)


async def _run_with_claude(spec: TripSpecification) -> Itinerary:
    """Run orchestration via Claude tool-use loop."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": (
                f"Plan this trip and search for all flights, ferries, and accommodation:\n\n"
                f"{spec.model_dump_json(indent=2)}"
            ),
        }
    ]

    research_results: dict[str, Any] = {}

    # Tool-use loop (max 10 iterations)
    for _ in range(10):
        response = client.messages.create(
            model=ORCHESTRATOR_MODEL,
            max_tokens=4096,
            system=ORCHESTRATOR_SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # Process response
        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await _execute_tool(block.name, block.input)
                    research_results[f"{block.name}_{block.id}"] = result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, default=str),
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    # Synthesize into itinerary
    return await _synthesize_itinerary(spec, research_results)


def build_research_tasks(spec: TripSpecification) -> dict[str, Any]:
    """Build research coroutine dict from spec without awaiting."""
    research_tasks: dict[str, Any] = {}
    current_date = spec.start_date

    for origin in spec.origins:
        origin_code = origin.airport_code or origin.city[:3].upper()

        # Skip if origin is the hub city (e.g., Athens crew doesn't fly to Athens)
        if origin_code == spec.hub_airport:
            continue

        # Flights: origin → hub
        research_tasks[f"flights_{origin.city}_to_{spec.hub_city}"] = search_flights(
            origin=origin_code,
            destination=spec.hub_airport,
            date_from=spec.start_date,
            adults=origin.num_travelers,
        )

        # Return flights: hub → origin
        research_tasks[f"flights_{spec.hub_city}_to_{origin.city}"] = search_flights(
            origin=spec.hub_airport,
            destination=origin_code,
            date_from=spec.end_date,
            adults=origin.num_travelers,
        )

    # Hub → first island (flight if airport exists, otherwise ferry)
    first_stop = spec.stops[0]
    island_info = resolve_island(first_stop.island)

    if island_info and island_info.airport_code:
        research_tasks[f"flights_{spec.hub_city}_to_{first_stop.island}"] = search_flights(
            origin=spec.hub_airport,
            destination=island_info.airport_code,
            date_from=spec.start_date,
        )

    # Ferry from hub to first island
    if island_info and island_info.port_code:
        research_tasks[f"ferries_hub_to_{first_stop.island}"] = search_ferries(
            origin_port="PIR",
            destination_port=island_info.port_code,
            travel_date=spec.start_date,
        )

    # Inter-island ferries
    for i in range(len(spec.stops) - 1):
        stop_a = spec.stops[i]
        stop_b = spec.stops[i + 1]
        info_a = resolve_island(stop_a.island)
        info_b = resolve_island(stop_b.island)

        transfer_date = current_date + timedelta(days=stop_a.nights)

        if info_a and info_b and info_a.port_code and info_b.port_code:
            research_tasks[f"ferries_{stop_a.island}_to_{stop_b.island}"] = search_ferries(
                origin_port=info_a.port_code,
                destination_port=info_b.port_code,
                travel_date=transfer_date,
            )

        current_date = transfer_date

    # Return ferry from last island
    last_stop = spec.stops[-1]
    last_info = resolve_island(last_stop.island)
    if last_info and last_info.port_code:
        return_date = spec.end_date
        research_tasks[f"ferries_{last_stop.island}_to_hub"] = search_ferries(
            origin_port=last_info.port_code,
            destination_port="PIR",
            travel_date=return_date,
        )

    # Accommodation for each stop
    current_date = spec.start_date
    for stop in spec.stops:
        checkin = current_date
        checkout = current_date + timedelta(days=stop.nights)
        research_tasks[f"accommodation_{stop.island}"] = search_accommodation(
            island=stop.island,
            checkin=checkin,
            checkout=checkout,
        )
        current_date = checkout

    return research_tasks


async def _run_deterministic(spec: TripSpecification) -> Itinerary:
    """Run deterministic research pipeline without Claude API."""
    console.print("\n[bold cyan]Running research pipeline...[/bold cyan]")

    tasks = build_research_tasks(spec)

    # Run all research in parallel
    results = await run_parallel_research(tasks)

    # Build itinerary from results
    return _build_itinerary(spec, results)


async def _execute_tool(name: str, params: dict[str, Any]) -> Any:
    """Execute a tool call from the Claude orchestrator."""
    console.print(f"  [dim]Tool: {name}({json.dumps(params, default=str)})[/dim]")

    if name == "search_flights":
        results = await search_flights(
            origin=params["origin"],
            destination=params["destination"],
            date_from=date.fromisoformat(params["date"]),
            adults=params.get("adults", 1),
        )
        return [f.model_dump() for f in results]

    elif name == "search_ferries":
        results = await search_ferries(
            origin_port=params["origin_port"],
            destination_port=params["destination_port"],
            travel_date=date.fromisoformat(params["date"]),
            passengers=params.get("passengers", 1),
        )
        return [f.model_dump() for f in results]

    elif name == "search_accommodation":
        results = await search_accommodation(
            island=params["island"],
            checkin=date.fromisoformat(params["checkin"]),
            checkout=date.fromisoformat(params["checkout"]),
            guests=params.get("guests", 2),
        )
        return [a.model_dump() for a in results]

    elif name == "get_island_info":
        info = resolve_island(params["island"])
        return info.model_dump() if info else {"error": f"Island {params['island']} not found"}

    return {"error": f"Unknown tool: {name}"}


async def _synthesize_itinerary(
    spec: TripSpecification,
    research: dict[str, Any],
) -> Itinerary:
    """Use Claude to synthesize research results into a structured itinerary."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prefs_section = ""
    if spec.rich_preferences:
        prefs_section = (
            f"\n\nUser preferences (use these to write preference-aware descriptions, "
            f"highlight relevant activities, and note budget-appropriate options):\n"
            f"{spec.rich_preferences.model_dump_json(indent=2)}"
        )

    response = client.messages.create(
        model=ORCHESTRATOR_MODEL,
        max_tokens=8000,
        system=ITINERARY_SYNTHESIS_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Trip specification:\n{spec.model_dump_json(indent=2)}\n\n"
                f"Research results:\n{json.dumps(research, indent=2, default=str)}"
                f"{prefs_section}"
            ),
        }],
    )

    text = response.content[0].text
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]

    data = json.loads(text)
    return Itinerary(**data)


def _sort_by_preferences(
    options: list[AccommodationOption],
    prefs: TripPreferences | None,
) -> list[AccommodationOption]:
    """Score and sort accommodation options by preference alignment."""
    if not prefs or not options:
        return options

    def score(opt: AccommodationOption) -> float:
        s = 0.0
        features_lower = " ".join(f.lower() for f in opt.features)
        name_lower = opt.name.lower()
        combined = features_lower + " " + name_lower

        # Budget fit: penalize if over max_per_night
        if prefs.max_per_night_eur and opt.price_per_night > 0:
            if opt.price_per_night <= prefs.max_per_night_eur:
                s += 20
            else:
                overshoot = opt.price_per_night / prefs.max_per_night_eur
                s -= min(overshoot * 10, 30)

        # Style match
        for style in prefs.accommodation_styles:
            if style.lower() in combined:
                s += 15

        # Activity relevance
        activity_keywords = {
            "beach": ["beach", "sea view", "waterfront", "seafront"],
            "boat_tours": ["port", "marina", "harbor"],
            "food_and_wine": ["restaurant", "kitchen", "dining"],
            "hiking": ["mountain", "trail", "nature"],
        }
        for activity in prefs.activities:
            keywords = activity_keywords.get(activity, [activity.replace("_", " ")])
            for kw in keywords:
                if kw in combined:
                    s += 10
                    break

        # Rating bonus
        if opt.rating > 0:
            s += (opt.rating / opt.rating_max) * 10

        return s

    return sorted(options, key=score, reverse=True)


def _build_itinerary(spec: TripSpecification, results: dict[str, Any]) -> Itinerary:
    """Build itinerary deterministically from research results."""
    days: list[DayPlan] = []
    accommodation_sections: list[AccommodationSection] = []
    current_date = spec.start_date
    route_summary = [spec.origins[0].city if spec.origins else "Origin", spec.hub_city]

    # ── Day 1: Travel to first island ──
    first_stop = spec.stops[0]
    first_info = resolve_island(first_stop.island)
    route_summary.append(first_stop.island)

    transport_legs = []

    # International flights
    for origin in spec.origins:
        key = f"flights_{origin.city}_to_{spec.hub_city}"
        flights = results.get(key)
        if isinstance(flights, list):
            flight_options = [FlightOption(**f) if isinstance(f, dict) else f for f in flights]
            airlines = [f.airline for f in flight_options[:4]]
            prices = [f for f in flight_options if f.price_amount > 0]
            price_str = ""
            if prices:
                lo = min(f.price_amount for f in prices)
                hi = max(f.price_amount for f in prices)
                cur = prices[0].price_currency
                sym = "£" if cur == "GBP" else "€"
                price_str = f"{sym}{lo:.0f}&ndash;{hi:.0f}"

            transport_legs.append(TransportLeg(
                mode=TransportMode.FLIGHT,
                origin=origin.city,
                destination=spec.hub_city,
                description=f"{origin.city} to {spec.hub_city} &middot; 3h 30m direct",
                price_display=price_str,
                options=flight_options,
                notes=", ".join(airlines) if airlines else "",
            ))

    # Hub to first island flight
    hub_flight_key = f"flights_{spec.hub_city}_to_{first_stop.island}"
    hub_flights = results.get(hub_flight_key)
    if isinstance(hub_flights, list) and hub_flights:
        flight_options = [FlightOption(**f) if isinstance(f, dict) else f for f in hub_flights]
        prices = [f for f in flight_options if f.price_amount > 0]
        price_str = ""
        if prices:
            lo = min(f.price_amount for f in prices)
            hi = max(f.price_amount for f in prices)
            price_str = f"&euro;{lo:.0f}&ndash;{hi:.0f}"

        transport_legs.append(TransportLeg(
            mode=TransportMode.FLIGHT,
            origin=spec.hub_city,
            destination=first_stop.island,
            description=f"{spec.hub_city} to {first_stop.island} &middot; 40 min",
            price_display=price_str,
            options=flight_options,
        ))

    # Ferry alternative to first island
    ferry_key = f"ferries_hub_to_{first_stop.island}"
    hub_ferries = results.get(ferry_key)
    if isinstance(hub_ferries, list) and hub_ferries:
        ferry_options = [FerryOption(**f) if isinstance(f, dict) else f for f in hub_ferries]
        best = ferry_options[0]
        dur_h = best.duration_minutes // 60
        dur_m = best.duration_minutes % 60
        dur_str = f"{dur_h}h {dur_m:02d}m" if dur_m else f"{dur_h}h"

        transport_legs.append(TransportLeg(
            mode=TransportMode.FERRY,
            origin="Piraeus",
            destination=first_stop.island,
            description=f"Piraeus to {first_stop.island} &middot; {best.operator} {dur_str} &middot; &euro;{best.price_amount:.0f}",
            notes="Ferry alternative",
            options=ferry_options,
        ))

    day1_sub = " &rarr; ".join([
        spec.origins[0].city if spec.origins else "Origin",
        spec.hub_city,
        first_stop.island,
    ])

    days.append(DayPlan(
        date_label=spec.start_date.strftime("%a %b %d"),
        title="Travel Day",
        subtitle=day1_sub,
        transport_legs=transport_legs,
        notes=[
            f"<strong>{spec.hub_city} crew:</strong> Same options &mdash; fly from {spec.hub_airport} or ferry from Piraeus. Coordinate arrival times."
        ] if len(spec.origins) > 1 else [],
    ))

    # ── Island stay days ──
    for i, stop in enumerate(spec.stops):
        info = resolve_island(stop.island)
        route_summary_name = stop.island
        if route_summary_name not in route_summary:
            route_summary.append(route_summary_name)

        checkin = current_date
        checkout = current_date + timedelta(days=stop.nights)
        car_note = "rent a car" if (info and info.needs_car) or stop.needs_car else "no car needed"

        days.append(DayPlan(
            date_label=f"{checkin.strftime('%b %d')}&ndash;{checkout.strftime('%d')}",
            title=stop.island,
            subtitle=f"{stop.nights} nights &middot; {car_note}",
            is_highlight=True,
            nights=stop.nights,
            needs_car=(info and info.needs_car) or stop.needs_car,
            highlights=_island_highlights(stop.island, spec.rich_preferences),
            notes=_island_notes(stop.island, checkin, checkout),
        ))

        # Inter-island transfer day
        if i < len(spec.stops) - 1:
            next_stop = spec.stops[i + 1]
            next_info = resolve_island(next_stop.island)
            transfer_date = checkout

            ferry_key = f"ferries_{stop.island}_to_{next_stop.island}"
            ferries = results.get(ferry_key)

            transfer_legs = []
            if isinstance(ferries, list) and ferries:
                ferry_options = [FerryOption(**f) if isinstance(f, dict) else f for f in ferries]
                best = ferry_options[0]
                dur_h = best.duration_minutes // 60
                dur_m = best.duration_minutes % 60
                dur_str = f"{dur_h}h" if not dur_m else f"{dur_h}h {dur_m:02d}m"

                transfer_legs.append(TransportLeg(
                    mode=TransportMode.FERRY,
                    origin=stop.island,
                    destination=next_stop.island,
                    description=f"{best.operator} &middot; ~{dur_str} &middot; &euro;{best.price_amount:.0f} per person",
                    options=ferry_options,
                ))

            days.append(DayPlan(
                date_label=transfer_date.strftime("%a %b %d"),
                title="Island Hop",
                subtitle=f"{stop.island} &rarr; {next_stop.island}",
                transport_legs=transfer_legs,
                notes=[
                    f"<strong>Important:</strong> This route may only run on certain days. Check sailing schedule for {transfer_date.strftime('%B %d')}."
                ],
            ))

        current_date = checkout

        # Accommodation section
        acc_key = f"accommodation_{stop.island}"
        acc_results = results.get(acc_key)
        if isinstance(acc_results, list):
            options = [
                AccommodationOption(**a) if isinstance(a, dict) else a
                for a in acc_results
            ]
            options = _sort_by_preferences(options, spec.rich_preferences)
            accommodation_sections.append(AccommodationSection(
                title=f"{stop.island} Accommodation &middot; {checkin.strftime('%b %d')}&ndash;{checkout.strftime('%d')} ({stop.nights} nights, 2 guests)",
                options=options,
            ))

    # ── Return day ──
    last_stop = spec.stops[-1]
    return_legs = []

    ferry_key = f"ferries_{last_stop.island}_to_hub"
    return_ferries = results.get(ferry_key)
    if isinstance(return_ferries, list) and return_ferries:
        ferry_options = [FerryOption(**f) if isinstance(f, dict) else f for f in return_ferries]
        best = ferry_options[0]
        dur_h = best.duration_minutes // 60
        dur_m = best.duration_minutes % 60
        dur_str = f"{dur_h}h {dur_m:02d}m" if dur_m else f"{dur_h}h"

        return_legs.append(TransportLeg(
            mode=TransportMode.FERRY,
            origin=last_stop.island,
            destination="Piraeus",
            description=f"{best.operator} &middot; ~{dur_str} &middot; &euro;{best.price_amount:.0f} per person",
            options=ferry_options,
        ))

    return_legs.append(TransportLeg(
        mode=TransportMode.TAXI,
        origin="Piraeus",
        destination=f"{spec.hub_city} Airport",
        description=f"Piraeus to {spec.hub_city} Airport &middot; ~45 min &middot; ~&euro;40",
    ))

    for origin in spec.origins:
        key = f"flights_{spec.hub_city}_to_{origin.city}"
        flights = results.get(key)
        if isinstance(flights, list) and flights:
            flight_options = [FlightOption(**f) if isinstance(f, dict) else f for f in flights]
            return_legs.append(TransportLeg(
                mode=TransportMode.FLIGHT,
                origin=spec.hub_city,
                destination=origin.city,
                description=f"{spec.hub_city} to {origin.city} (evening)",
                options=flight_options,
            ))

    return_sub = " &rarr; ".join([
        last_stop.island,
        spec.hub_city,
        spec.origins[0].city if spec.origins else "Home",
    ])

    days.append(DayPlan(
        date_label=spec.end_date.strftime("%a %b %d"),
        title="Return",
        subtitle=return_sub,
        transport_legs=return_legs,
        notes=[
            "<strong>Safer option:</strong> Take the evening ferry the day before, sleep near the airport, fly out in the morning. Removes all stress.",
            "<strong>Athens crew:</strong> You're home once you dock at Piraeus!",
        ] if len(spec.origins) > 1 else [
            "<strong>Safer option:</strong> Take the evening ferry the day before, sleep near the airport, fly out in the morning."
        ],
    ))

    # ── Cost breakdowns ──
    cost_breakdowns = _build_cost_breakdowns(spec, results)

    # ── Action items ──
    action_items = _build_action_items(spec)

    # ── Useful links ──
    useful_links = _build_useful_links(spec)

    route_summary.append(spec.origins[0].city if spec.origins else "Home")

    return Itinerary(
        title=spec.title,
        subtitle=" & ".join(s.island for s in spec.stops),
        date_range=f"{spec.start_date.strftime('%a %d %b')} &ndash; {spec.end_date.strftime('%a %d %b %Y')}",
        group_info=spec.group_description or f"{spec.total_travelers} travelers",
        route_summary=route_summary,
        days=days,
        accommodation_sections=accommodation_sections,
        cost_breakdowns=cost_breakdowns,
        action_items=action_items,
        useful_links=useful_links,
        generated_at=date.today().strftime("%b %Y"),
    )


def _island_highlights(island: str, prefs: TripPreferences | None = None) -> list[str]:
    """Return activity highlights for known islands, reordered by preferences."""
    highlights: dict[str, list[str]] = {
        "Milos": [
            "Sarakiniko (lunar landscape beach)",
            "Tsigrado &amp; Firiplaka (south coast gems)",
            "Kleftiko boat tour from Adamas (~&euro;60&ndash;120pp)",
            "Plaka village for sunset",
            "Paleochori (hot sand beach with tavernas)",
        ],
        "Koufonisia": [
            "Pori beach (best on the island, fine white sand)",
            "Italida &amp; Fanos beaches",
            "Chora village &mdash; tavernas, bars, bakeries",
            "Sea taxi around the island",
            "Walk everywhere &mdash; island is tiny",
        ],
        "Santorini": [
            "Oia sunset",
            "Fira to Oia hike along the caldera",
            "Red Beach &amp; White Beach",
            "Wine tasting at Santo Wines or Venetsanos",
            "Amoudi Bay for seafood",
        ],
        "Naxos": [
            "Portara (Temple of Apollo)",
            "Plaka beach (longest sandy beach in Cyclades)",
            "Halki village (Kitron distillery)",
            "Mountain villages (Apiranthos, Filoti)",
            "Windsurfing at Mikri Vigla",
        ],
        "Paros": [
            "Naoussa village &amp; old port",
            "Kolymbithres beach (sculpted rocks)",
            "Parikia old town &amp; Panagia Ekatontapiliani",
            "Golden Beach windsurfing",
            "Antiparos day trip &amp; cave",
        ],
    }
    items = highlights.get(island, [f"Explore {island}"])

    if prefs and prefs.activities:
        # Score each highlight by how many activity keywords it matches
        activity_kws = [a.replace("_", " ").lower() for a in prefs.activities]
        activity_kws += [a.replace("_and_", " ").lower() for a in prefs.activities]

        def relevance(h: str) -> int:
            h_lower = h.lower()
            return sum(1 for kw in activity_kws if kw in h_lower)

        items = sorted(items, key=relevance, reverse=True)

    return items


def _island_notes(island: str, checkin: date, checkout: date) -> list[str]:
    """Return contextual warnings for an island stay."""
    notes = []
    # Check for Aug 15 (Assumption of Mary)
    aug_15 = date(checkin.year, 8, 15)
    if checkin <= aug_15 <= checkout:
        notes.append(
            "<strong>Heads up:</strong> Aug 15 is Assumption of Mary &mdash; "
            "big Greek holiday, expect crowds and some places closed."
        )
    return notes


def _build_cost_breakdowns(
    spec: TripSpecification,
    results: dict[str, Any],
) -> list[CostBreakdown]:
    """Build per-origin cost breakdown tables."""
    breakdowns = []

    for origin in spec.origins:
        items = []

        # International flights
        key = f"flights_{origin.city}_to_{spec.hub_city}"
        flights = results.get(key)
        if isinstance(flights, list) and flights:
            options = [FlightOption(**f) if isinstance(f, dict) else f for f in flights]
            prices = [f.price_amount for f in options if f.price_amount > 0]
            if prices:
                cur = options[0].price_currency
                sym = "£" if cur == "GBP" else "€"
                items.append(CostLineItem(
                    label=f"Flights {origin.city} &harr; {spec.hub_city} (return)",
                    amount_display=f"{sym}{min(prices):.0f} &ndash; {max(prices):.0f}",
                ))

        # Hub to first island
        first = spec.stops[0]
        hub_key = f"flights_{spec.hub_city}_to_{first.island}"
        hub_flights = results.get(hub_key)
        if isinstance(hub_flights, list) and hub_flights:
            options = [FlightOption(**f) if isinstance(f, dict) else f for f in hub_flights]
            prices = [f.price_amount for f in options if f.price_amount > 0]
            if prices:
                items.append(CostLineItem(
                    label=f"Flight {spec.hub_city} &rarr; {first.island} (one way)",
                    amount_display=f"&euro;{min(prices):.0f} &ndash; {max(prices):.0f}",
                ))

        # Inter-island ferries
        for i in range(len(spec.stops) - 1):
            a, b = spec.stops[i], spec.stops[i + 1]
            key = f"ferries_{a.island}_to_{b.island}"
            ferries = results.get(key)
            if isinstance(ferries, list) and ferries:
                options = [FerryOption(**f) if isinstance(f, dict) else f for f in ferries]
                prices = [f.price_amount for f in options if f.price_amount > 0]
                if prices:
                    items.append(CostLineItem(
                        label=f"Ferry {a.island} &rarr; {b.island}",
                        amount_display=f"&euro;{min(prices):.0f} &ndash; {max(prices):.0f}",
                    ))

        # Return ferry
        last = spec.stops[-1]
        key = f"ferries_{last.island}_to_hub"
        ret_ferries = results.get(key)
        if isinstance(ret_ferries, list) and ret_ferries:
            options = [FerryOption(**f) if isinstance(f, dict) else f for f in ret_ferries]
            prices = [f.price_amount for f in options if f.price_amount > 0]
            if prices:
                items.append(CostLineItem(
                    label=f"Ferry {last.island} &rarr; Piraeus",
                    amount_display=f"&euro;{min(prices):.0f} &ndash; {max(prices):.0f}",
                ))

        # Taxi
        items.append(CostLineItem(
            label=f"Taxi Piraeus &rarr; {spec.hub_airport} airport",
            amount_display="&euro;20 (your half)",
        ))

        # Accommodation per stop
        current = spec.start_date
        for stop in spec.stops:
            key = f"accommodation_{stop.island}"
            acc = results.get(key)
            if isinstance(acc, list) and acc:
                options = [AccommodationOption(**a) if isinstance(a, dict) else a for a in acc]
                prices = [a.price_per_night for a in options if a.price_per_night > 0]
                if prices:
                    lo = min(prices) * stop.nights / 2
                    hi = max(prices) * stop.nights / 2
                    items.append(CostLineItem(
                        label=f"{stop.island} accommodation ({stop.nights} nights, your half)",
                        amount_display=f"${lo:.0f} &ndash; ${hi:.0f}",
                    ))
            current += timedelta(days=stop.nights)

        # Car rental for islands that need it
        for stop in spec.stops:
            info = resolve_island(stop.island)
            if (info and info.needs_car) or stop.needs_car:
                items.append(CostLineItem(
                    label=f"Car rental {stop.island} ({stop.nights} days, split)",
                    amount_display=f"&euro;{stop.nights * 30} &ndash; {stop.nights * 50}",
                ))

        # Total estimate
        breakdowns.append(CostBreakdown(
            origin_label=f"{origin.city} {'couple' if origin.num_travelers == 2 else 'group'}",
            line_items=items,
            total_display="&euro;700 &ndash; 1,500",
        ))

    return breakdowns


def _build_action_items(spec: TripSpecification) -> list[ActionItem]:
    """Build urgency-ordered booking action items."""
    items = []
    priority = 1

    # Tiny islands first
    for stop in spec.stops:
        info = resolve_island(stop.island)
        if info and info.description and "tiny" in info.description.lower():
            checkin = spec.start_date
            for s in spec.stops:
                if s.island == stop.island:
                    break
                checkin += timedelta(days=s.nights)
            checkout = checkin + timedelta(days=stop.nights)

            items.append(ActionItem(
                priority=priority,
                title=f"{stop.island} accommodation",
                reason=f"Only ~20 places on the entire island. August sells out completely.",
                links=[
                    ("Search Airbnb", airbnb_search_url(stop.island, checkin, checkout)),
                    ("Search Booking.com", booking_search_url(stop.island, checkin, checkout)),
                ],
            ))
            priority += 1

    # Small island flights
    for stop in spec.stops:
        info = resolve_island(stop.island)
        if info and info.airport_code:
            items.append(ActionItem(
                priority=priority,
                title=f"{spec.hub_city} &rarr; {stop.island} flight",
                reason=f"Tiny 70-seat turboprops, sells out months ahead.",
                links=[
                    ("Olympic Air", f"https://www.olympicair.com/en/flights-from-{spec.hub_city.lower()}-to-{stop.island.lower()}"),
                    ("Sky Express", f"https://www.skyexpress.gr/en/flights-from-{spec.hub_city.lower()}-to-{stop.island.lower()}"),
                ],
            ))
            priority += 1

    # Other island accommodation
    current = spec.start_date
    for stop in spec.stops:
        checkin = current
        checkout = current + timedelta(days=stop.nights)
        info = resolve_island(stop.island)
        already_added = any(a.title.startswith(stop.island) for a in items)
        if not already_added:
            items.append(ActionItem(
                priority=priority,
                title=f"{stop.island} accommodation",
                reason=f"Peak August — book early.",
                links=[
                    ("Search Holidu", holidu_search_url(stop.island, checkin, checkout)),
                    ("Search Airbnb", airbnb_search_url(stop.island, checkin, checkout)),
                ],
            ))
            priority += 1
        current = checkout

    # International flights
    for origin in spec.origins:
        items.append(ActionItem(
            priority=priority,
            title=f"{origin.city} &harr; {spec.hub_city} flights",
            reason="Set a price alert.",
            links=[
                ("Skyscanner", "https://www.skyscanner.net"),
                ("Google Flights", "https://www.google.com/travel/flights"),
            ],
        ))
        priority += 1

    # Ferries
    items.append(ActionItem(
        priority=priority,
        title="Ferries",
        reason="Summer timetables published closer to date.",
        links=[
            ("Ferryhopper", "https://www.ferryhopper.com"),
            ("SeaJets", "https://www.seajets.com"),
        ],
    ))
    priority += 1

    # Car rental
    for stop in spec.stops:
        info = resolve_island(stop.island)
        if (info and info.needs_car) or stop.needs_car:
            items.append(ActionItem(
                priority=priority,
                title=f"Car rental in {stop.island}",
                reason="Also sells out in August. Search closer to the date.",
                links=[],
            ))
            priority += 1

    return items


def _build_useful_links(spec: TripSpecification) -> list[UsefulLink]:
    """Build the useful links grid."""
    links = [
        UsefulLink(category="Flights", name="Skyscanner", url="https://www.skyscanner.net"),
        UsefulLink(category="Flights", name="Google Flights", url="https://www.google.com/travel/flights"),
        UsefulLink(category="Ferries", name="Ferryhopper", url="https://www.ferryhopper.com"),
        UsefulLink(category="Ferries", name="SeaJets", url="https://www.seajets.com"),
    ]

    for stop in spec.stops:
        links.append(UsefulLink(
            category=f"{stop.island} Stays",
            name="Airbnb",
            url=f"https://www.airbnb.com/{stop.island.lower()}-greece/stays",
        ))

    for stop in spec.stops:
        links.append(UsefulLink(
            category=f"{stop.island} Hotels",
            name="Booking.com",
            url=f"https://www.booking.com/city/gr/{stop.island.lower()}.html",
        ))

    return links
