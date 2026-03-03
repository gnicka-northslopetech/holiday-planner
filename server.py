"""FastAPI server — serves the Wanderlust prototype with live backend data."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import date, time, datetime
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from config import ANTHROPIC_API_KEY
from models.trip import TripSpecification, TripPreferences
from agents.orchestrator import (
    build_research_tasks,
    _build_itinerary,
    extract_trip_spec,
    generate_preference_question,
    extract_structured_preferences,
    generate_preference_summary,
    PREFERENCE_CATEGORIES,
)

log = logging.getLogger("tripforge")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="TripForge")

PROJECT_ROOT = Path(__file__).parent
TRIPS_DIR = PROJECT_ROOT / "trips"


def _json_serial(obj: Any) -> Any:
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, time):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


# ── Endpoints ──


@app.get("/api/default-spec")
async def default_spec():
    """Load the default trip spec (greece-2026.yaml) as JSON."""
    yaml_path = TRIPS_DIR / "greece-2026.yaml"
    if not yaml_path.exists():
        raise HTTPException(404, "Default trip spec not found")
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    spec = TripSpecification(**data)
    return json.loads(spec.model_dump_json())


class BriefRequest(BaseModel):
    text: str


@app.post("/api/extract-brief")
async def api_extract_brief(req: BriefRequest):
    """Use Claude NLP to extract a TripSpecification from free-text."""
    if not ANTHROPIC_API_KEY:
        raise HTTPException(501, "ANTHROPIC_API_KEY not set — use /api/default-spec instead")
    spec = await extract_trip_spec(req.text)
    return json.loads(spec.model_dump_json())


class ResearchRequest(BaseModel):
    spec: dict


@app.post("/api/research")
async def api_research(req: ResearchRequest):
    """Run research pipeline and stream SSE progress."""
    spec = TripSpecification(**req.spec)

    async def event_stream():
        # Build coroutines
        task_dict = build_research_tasks(spec)
        total = len(task_dict)
        results: dict[str, Any] = {}
        done_count = 0

        # Use a queue to bridge task completions into the SSE generator
        queue: asyncio.Queue[str] = asyncio.Queue()

        async def run_task(name: str, coro: Any) -> None:
            nonlocal done_count
            log.info("START  %s", name)
            try:
                results[name] = await asyncio.wait_for(coro, timeout=25)
                # Summarize result
                r = results[name]
                if isinstance(r, list):
                    log.info("DONE   %s → %d results", name, len(r))
                else:
                    log.info("DONE   %s → %s", name, type(r).__name__)
            except asyncio.TimeoutError:
                log.warning("TIMEOUT %s after 25s — using empty result", name)
                results[name] = []
            except Exception as e:
                log.error("FAIL   %s → %s", name, e)
                results[name] = str(e)
            done_count += 1
            progress = json.dumps({
                "step": name,
                "done": done_count,
                "total": total,
            })
            await queue.put(f"event: progress\ndata: {progress}\n\n")

        # Start all tasks
        tasks = [
            asyncio.create_task(run_task(name, coro))
            for name, coro in task_dict.items()
        ]

        # Yield progress as tasks complete
        for _ in range(total):
            msg = await queue.get()
            yield msg

        # Wait for all tasks to be fully done
        await asyncio.gather(*tasks)

        # Build itinerary
        try:
            itinerary = _build_itinerary(spec, results)
            itin_json = json.dumps(
                json.loads(itinerary.model_dump_json()),
                default=_json_serial,
            )
            yield f"event: complete\ndata: {itin_json}\n\n"
        except Exception as e:
            log.error("Failed to build itinerary: %s", e)
            error_json = json.dumps({"error": str(e)})
            yield f"event: error\ndata: {error_json}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ── Preferences session store ──

import uuid

_pref_sessions: dict[str, dict] = {}


class PreferencesStartRequest(BaseModel):
    spec: dict


class PreferencesAnswerRequest(BaseModel):
    session_id: str
    answer: str


class PreferencesConfirmRequest(BaseModel):
    session_id: str


@app.post("/api/preferences/start")
async def api_preferences_start(req: PreferencesStartRequest):
    """Start a preference-gathering session. Returns first question + session ID."""
    if not ANTHROPIC_API_KEY:
        raise HTTPException(501, "ANTHROPIC_API_KEY not set")

    spec = TripSpecification(**req.spec)
    session_id = str(uuid.uuid4())

    question_data = await generate_preference_question(spec, PREFERENCE_CATEGORIES[0], [])

    _pref_sessions[session_id] = {
        "spec": req.spec,
        "answers": [],
        "step": 0,
        "preferences": None,
        "summary": None,
    }

    return {
        "session_id": session_id,
        "question": question_data.get("question", ""),
        "options": question_data.get("options", []),
        "step": 1,
        "total_steps": len(PREFERENCE_CATEGORIES) + 1,  # +1 for summary
    }


@app.post("/api/preferences/answer")
async def api_preferences_answer(req: PreferencesAnswerRequest):
    """Submit an answer, get next question or final summary."""
    session = _pref_sessions.get(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    spec = TripSpecification(**session["spec"])
    step = session["step"]
    category = PREFERENCE_CATEGORIES[step]

    # Store this answer
    session["answers"].append({
        "category": category,
        "answer": req.answer,
    })
    session["step"] = step + 1

    next_step = step + 1

    if next_step < len(PREFERENCE_CATEGORIES):
        # Generate next question
        question_data = await generate_preference_question(
            spec, PREFERENCE_CATEGORIES[next_step], session["answers"]
        )
        return {
            "type": "question",
            "question": question_data.get("question", ""),
            "options": question_data.get("options", []),
            "step": next_step + 1,
            "total_steps": len(PREFERENCE_CATEGORIES) + 1,
        }
    else:
        # All questions answered — extract preferences + generate summary
        prefs = await extract_structured_preferences(spec, session["answers"])
        summary = await generate_preference_summary(spec, prefs)

        session["preferences"] = json.loads(prefs.model_dump_json())
        session["summary"] = summary

        return {
            "type": "summary",
            "summary": summary,
            "step": len(PREFERENCE_CATEGORIES) + 1,
            "total_steps": len(PREFERENCE_CATEGORIES) + 1,
        }


@app.post("/api/preferences/confirm")
async def api_preferences_confirm(req: PreferencesConfirmRequest):
    """Confirm preferences and return enriched spec."""
    session = _pref_sessions.get(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    spec_data = dict(session["spec"])
    if session["preferences"]:
        spec_data["rich_preferences"] = session["preferences"]

    # Clean up session
    del _pref_sessions[req.session_id]

    return {"spec": spec_data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
