"""Parallel research execution — run flight, ferry, accommodation searches concurrently."""

from __future__ import annotations

import asyncio
from typing import Any

from rich.console import Console

console = Console()


async def run_parallel_research(
    tasks: dict[str, Any],
) -> dict[str, Any]:
    """Run multiple async research coroutines in parallel.

    Args:
        tasks: Dict mapping task names to coroutines.
               e.g. {"flights_london": search_flights(...), "ferries_milos": search_ferries(...)}

    Returns:
        Dict mapping task names to results (or Exception on failure).
    """
    results: dict[str, Any] = {}

    async def _run_one(name: str, coro: Any) -> None:
        try:
            console.print(f"  [dim]Researching {name}...[/dim]")
            results[name] = await coro
            console.print(f"  [green]Done:[/green] {name}")
        except Exception as e:
            console.print(f"  [red]Failed:[/red] {name}: {e}")
            results[name] = e

    await asyncio.gather(*[_run_one(name, coro) for name, coro in tasks.items()])

    return results
