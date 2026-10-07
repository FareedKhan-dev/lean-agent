import time


class Auth:
    """See SPEC.md."""

    def __init__(self, clock=time.time):
        self.clock = clock
