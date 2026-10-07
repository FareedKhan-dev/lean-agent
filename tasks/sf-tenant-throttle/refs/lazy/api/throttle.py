from collections import deque


class Throttle:
    """At most `limit` requests per tenant in any `window_s`-second window."""

    def __init__(self, limit, window_s):
        self.limit = limit
        self.window_s = window_s
        self.times = deque()

    def allow(self, tenant, now):
        """True if this request from `tenant` at time `now` (seconds) may go ahead."""
        while self.times and self.times[0] <= now - self.window_s:
            self.times.popleft()
        if len(self.times) >= self.limit:
            return False
        self.times.append(now)
        return True
