import threading
import time

import register


class CacheEntry:
    """A cached value and the time it was stored."""

    def __init__(self, value, stored_at):
        self.value = value
        self.stored_at = stored_at


class DistrictCache:
    """Thread-safe TTL cache with a size limit and hit/miss statistics."""

    def __init__(self, max_size=10_000, ttl_seconds=3600.0, enable_stats=True):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.enable_stats = enable_stats
        self._entries = {}
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        with self._lock:
            entry = self._entries.get(key)
            if entry is None or time.monotonic() - entry.stored_at > self.ttl_seconds:
                if self.enable_stats:
                    self.misses += 1
                return None, False
            if self.enable_stats:
                self.hits += 1
            return entry.value, True

    def put(self, key, value):
        with self._lock:
            if len(self._entries) >= self.max_size:
                oldest = min(self._entries, key=lambda k: self._entries[k].stored_at)
                del self._entries[oldest]
            self._entries[key] = CacheEntry(value, time.monotonic())

    def clear(self):
        with self._lock:
            self._entries.clear()


_cache = DistrictCache()


def normalise(postcode):
    """'sw1a 1aa' -> 'SW1A1AA'"""
    return postcode.replace(" ", "").upper()


def lookup_district(postcode):
    """Return the district for a postcode, or None if the register does not know it."""
    code = normalise(postcode)
    value, found = _cache.get(code)
    if found:
        return value
    value = register.scan(code)
    _cache.put(code, value)
    return value
