"""Configuration and API keys — loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

# Project paths
PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output" / "generated"
CACHE_DIR = PROJECT_ROOT / ".cache"

# API Keys (from environment)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
KIWI_API_KEY = os.environ.get("KIWI_API_KEY", "")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
BOOKING_API_KEY = os.environ.get("BOOKING_API_KEY", "")

# LLM settings
ORCHESTRATOR_MODEL = "claude-sonnet-4-20250514"
EXTRACTION_MODEL = "claude-haiku-4-5-20251001"

# Cache TTLs (seconds)
CACHE_TTL_FLIGHTS = 3600        # 1 hour
CACHE_TTL_FERRIES = 86400       # 24 hours
CACHE_TTL_ACCOMMODATION = 3600  # 1 hour

# Rate limits (requests per minute)
RATE_LIMIT_KIWI = 30
RATE_LIMIT_FERRYHOPPER = 10
RATE_LIMIT_BOOKING = 20
