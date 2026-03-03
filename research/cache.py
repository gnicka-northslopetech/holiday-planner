"""Disk-based caching with per-source TTLs."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import diskcache

from config import CACHE_DIR

_cache: diskcache.Cache | None = None


def get_cache() -> diskcache.Cache:
    global _cache
    if _cache is None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache = diskcache.Cache(str(CACHE_DIR))
    return _cache


def cache_key(source: str, **params: Any) -> str:
    """Generate a deterministic cache key from source name and params."""
    param_str = json.dumps(params, sort_keys=True, default=str)
    h = hashlib.sha256(f"{source}:{param_str}".encode()).hexdigest()[:16]
    return f"{source}:{h}"


def cached_get(source: str, ttl: int, **params: Any) -> Any | None:
    """Return cached value if it exists and hasn't expired."""
    c = get_cache()
    key = cache_key(source, **params)
    return c.get(key)


def cached_set(source: str, value: Any, ttl: int, **params: Any) -> None:
    """Store a value in cache with TTL."""
    c = get_cache()
    key = cache_key(source, **params)
    c.set(key, value, expire=ttl)
