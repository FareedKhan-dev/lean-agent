import threading
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import asdict, dataclass


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    evictions: int = 0


@dataclass
class Entry:
    value: object
    expires_at: float


class EvictionPolicy(ABC):
    @abstractmethod
    def touch(self, key):
        ...

    @abstractmethod
    def victim(self):
        ...

    @abstractmethod
    def forget(self, key):
        ...


class LRUPolicy(EvictionPolicy):
    def __init__(self):
        self._order = OrderedDict()

    def touch(self, key):
        self._order[key] = None
        self._order.move_to_end(key)

    def victim(self):
        return next(iter(self._order))

    def forget(self, key):
        self._order.pop(key, None)


class TTLCache:
    """Entries expire `ttl` seconds after they are set; at most `max_size` entries, the least
    recently used evicted first; stats() counts hits, misses and evictions."""

    def __init__(self, max_size, ttl, clock=time.monotonic, policy=None, on_evict=None):
        self.max_size, self.ttl, self.clock = max_size, ttl, clock
        self.policy = policy or LRUPolicy()
        self.on_evict = on_evict or (lambda key, value: None)
        self._entries = {}
        self._stats = CacheStats()
        self._lock = threading.RLock()

    def _expired(self, entry):
        return entry.expires_at <= self.clock()

    def get(self, key, default=None):
        with self._lock:
            entry = self._entries.get(key)
            if entry is None or self._expired(entry):
                if entry is not None:
                    del self._entries[key]
                    self.policy.forget(key)
                self._stats.misses += 1
                return default
            self.policy.touch(key)
            self._stats.hits += 1
            return entry.value

    def set(self, key, value):
        with self._lock:
            if key not in self._entries and len(self._entries) >= self.max_size:
                victim = self.policy.victim()
                self.on_evict(victim, self._entries.pop(victim).value)
                self.policy.forget(victim)
                self._stats.evictions += 1
            self._entries[key] = Entry(value, self.clock() + self.ttl)
            self.policy.touch(key)

    def stats(self):
        with self._lock:
            return asdict(self._stats)
