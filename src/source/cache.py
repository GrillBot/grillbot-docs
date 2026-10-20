import logging
import os
import threading
import time
from typing import Any, Callable, Dict, Optional, Tuple

# How long downloaded package data (csproj, package.json, ...) stays fresh.
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "7200"))
# Online status changes quickly and is checked on every page render, so it gets a much shorter lifetime.
HEALTH_TTL_SECONDS = int(os.environ.get("HEALTH_TTL_SECONDS", "30"))
# When a refresh fails, the previous value is served for at most this long.
STALE_LIMIT_SECONDS = 24 * 60 * 60
# After a failed refresh the stale value is kept for this long before the next attempt.
RETRY_SECONDS = 60


class Cache:
    """Thread-safe in-process TTL cache with single-flight loading and stale-on-error."""

    def __init__(self) -> None:
        # key -> (value, loaded_at, expires_at), all times from time.monotonic().
        self._items: Dict[str, Tuple[Any, float, float]] = dict()
        self._key_locks: Dict[str, threading.Lock] = dict()
        self._lock = threading.Lock()

    def get_or_load(
        self, key: str, loader: Callable[[], Any], ttl: Optional[int] = None
    ) -> Any:
        """Return the cached value for the key, calling the loader when it is missing or expired.

        Concurrent callers for the same key wait for one load instead of each hitting the upstream.
        If the loader raises and a value younger than STALE_LIMIT_SECONDS exists, that value is
        returned (and the next attempt is delayed by RETRY_SECONDS); otherwise the error propagates.
        """
        ttl = CACHE_TTL_SECONDS if ttl is None else ttl

        item = self._read(key)
        if item is not None and item[2] > time.monotonic():
            return item[0]

        with self._key_lock(key):
            item = self._read(key)
            now = time.monotonic()
            if item is not None and item[2] > now:
                return item[0]

            try:
                value = loader()
            except Exception:
                if item is None or now - item[1] > STALE_LIMIT_SECONDS:
                    raise
                logging.warning(
                    f"Refreshing {key} failed, serving data from {int(now - item[1])} s ago.",
                    exc_info=True,
                )
                self._write(key, (item[0], item[1], now + RETRY_SECONDS))
                return item[0]

            now = time.monotonic()
            self._write(key, (value, now, now + ttl))
            return value

    def _read(self, key: str) -> Optional[Tuple[Any, float, float]]:
        with self._lock:
            return self._items.get(key)

    def _write(self, key: str, item: Tuple[Any, float, float]) -> None:
        with self._lock:
            self._items[key] = item

    def _key_lock(self, key: str) -> threading.Lock:
        with self._lock:
            return self._key_locks.setdefault(key, threading.Lock())


cache = Cache()
