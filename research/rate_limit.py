"""Simple async rate limiter — token bucket per source."""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict


class RateLimiter:
    """Token-bucket rate limiter. One instance per source."""

    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.interval = 60.0 / requests_per_minute
        self._last_request = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            wait = self._last_request + self.interval - now
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_request = time.monotonic()


# Global registry of rate limiters
_limiters: dict[str, RateLimiter] = {}


def get_limiter(source: str, rpm: int) -> RateLimiter:
    if source not in _limiters:
        _limiters[source] = RateLimiter(rpm)
    return _limiters[source]
