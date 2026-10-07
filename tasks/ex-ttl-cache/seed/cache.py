import time


class TTLCache:
    """Entries expire `ttl` seconds after they are set; at most `max_size` entries, the least
    recently used evicted first; stats() counts hits, misses and evictions."""

    def __init__(self, max_size, ttl, clock=time.monotonic):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def stats(self):
        raise NotImplementedError
