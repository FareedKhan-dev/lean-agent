from collections import defaultdict, deque


class Throttle:
    """At most `limit` requests per tenant in any `window_s`-second window."""

    def __init__(self, limit, window_s):
        self.limit = limit
        self.window_s = window_s
        self.seen = defaultdict(deque)

    def allow(self, tenant, now):
        """True if this request from `tenant` at time `now` (seconds) may go ahead."""
        times = self.seen[tenant]
        while times and times[0] <= now - self.window_s:
            times.popleft()
        if len(times) >= self.limit:
            return False
        times.append(now)
        return True
