"""TripForge CLI — AI Holiday Planner for Greek Islands."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.panel import Panel

from config import ANTHROPIC_API_KEY
from models.trip import TripSpecification
from agents.orchestrator import run_orchestrator, extract_trip_spec
from output.renderer import render_itinerary
from output.share import get_share_url

app = typer.Typer(
    name="tripforge",
    help="TripForge — AI Holiday Planner for Greek Islands",
    add_completion=False,
)
console = Console()


@app.command()
def plan(
    input_file: Path = typer.Argument(
        ...,
        help="Path to trip YAML file or text brief",
        exists=True,
    ),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output HTML file path (default: auto-generated)",
    ),
    no_api: bool = typer.Option(
        False,
        "--no-api",
        help="Skip live API calls, use mock/static data only",
    ),
) -> None:
    """Plan a trip from a YAML specification file."""
    console.print(Panel.fit(
        "[bold cyan]TripForge[/bold cyan] — AI Holiday Planner",
        border_style="cyan",
    ))

    # Load trip specification
    console.print("\n[bold]Loading trip specification...[/bold]")
    spec = _load_spec(input_file)

    console.print(f"  Title: [cyan]{spec.title}[/cyan]")
    console.print(f"  Dates: {spec.start_date} → {spec.end_date}")
    console.print(f"  Stops: {' → '.join(s.island for s in spec.stops)}")
    console.print(f"  Group: {spec.group_description} ({spec.total_travelers} travelers)")
    console.print(f"  Origins: {', '.join(o.city for o in spec.origins)}")

    if no_api:
        console.print("\n[yellow]Running in offline mode (mock data).[/yellow]")

    # Run orchestrator
    console.print("\n[bold]Running research pipeline...[/bold]")
    itinerary = asyncio.run(run_orchestrator(spec))

    # Render HTML
    console.print("\n[bold]Rendering itinerary...[/bold]")
    html_path = render_itinerary(itinerary, output)

    console.print(f"\n[bold green]Done![/bold green] Itinerary saved to:")
    console.print(f"  [cyan]{html_path}[/cyan]")
    console.print(f"  [dim]{get_share_url(html_path)}[/dim]")


@app.command()
def brief(
    text: str = typer.Argument(
        ...,
        help="Free-text trip brief (e.g. '3 couples, London and Athens to Milos and Koufonisia, Aug 14-21 2026')",
    ),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output HTML file path",
    ),
) -> None:
    """Plan a trip from a free-text description (requires Claude API key)."""
    if not ANTHROPIC_API_KEY:
        console.print("[red]Error:[/red] ANTHROPIC_API_KEY required for free-text input.")
        console.print("Set it with: export ANTHROPIC_API_KEY=sk-...")
        console.print("Or use a YAML file instead: tripforge plan trips/greece-2026.yaml")
        raise typer.Exit(1)

    console.print(Panel.fit(
        "[bold cyan]TripForge[/bold cyan] — AI Holiday Planner",
        border_style="cyan",
    ))

    console.print("\n[bold]Extracting trip details from brief...[/bold]")
    spec = asyncio.run(extract_trip_spec(text))

    console.print(f"  Title: [cyan]{spec.title}[/cyan]")
    console.print(f"  Dates: {spec.start_date} → {spec.end_date}")
    console.print(f"  Stops: {' → '.join(s.island for s in spec.stops)}")

    console.print("\n[bold]Running research pipeline...[/bold]")
    itinerary = asyncio.run(run_orchestrator(spec))

    console.print("\n[bold]Rendering itinerary...[/bold]")
    html_path = render_itinerary(itinerary, output)

    console.print(f"\n[bold green]Done![/bold green]")
    console.print(f"  [cyan]{html_path}[/cyan]")


def _load_spec(path: Path) -> TripSpecification:
    """Load a TripSpecification from a YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return TripSpecification(**data)


if __name__ == "__main__":
    app()
