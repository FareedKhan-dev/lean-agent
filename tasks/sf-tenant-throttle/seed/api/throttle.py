class Throttle:
    """At most `limit` requests per tenant in any `window_s`-second window."""

    def __init__(self, limit, window_s):
        self.limit = limit
        self.window_s = window_s

    def allow(self, tenant, now):
        """True if this request from `tenant` at time `now` (seconds) may go ahead."""
        raise NotImplementedError
