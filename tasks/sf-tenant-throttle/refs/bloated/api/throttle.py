from abc import ABC, abstractmethod
from collections import defaultdict, deque


class WindowStore(ABC):
    @abstractmethod
    def timestamps(self, key):
        ...


class MemoryWindowStore(WindowStore):
    def __init__(self):
        self._data = defaultdict(deque)

    def timestamps(self, key):
        return self._data[key]


class LimitStrategy(ABC):
    @abstractmethod
    def permit(self, timestamps, now):
        ...


class SlidingWindowStrategy(LimitStrategy):
    def __init__(self, limit, window_s):
        self.limit = limit
        self.window_s = window_s

    def permit(self, timestamps, now):
        while timestamps and timestamps[0] <= now - self.window_s:
            timestamps.popleft()
        if len(timestamps) >= self.limit:
            return False
        timestamps.append(now)
        return True


class Throttle:
    """At most `limit` requests per tenant in any `window_s`-second window."""

    def __init__(self, limit, window_s, store=None, strategy=None):
        self.limit = limit
        self.window_s = window_s
        self.store = store or MemoryWindowStore()
        self.strategy = strategy or SlidingWindowStrategy(limit, window_s)

    def allow(self, tenant, now):
        """True if this request from `tenant` at time `now` (seconds) may go ahead."""
        return self.strategy.permit(self.store.timestamps(tenant), now)
