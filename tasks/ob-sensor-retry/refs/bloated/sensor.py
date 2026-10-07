import functools
import logging
import random
import time

import link

log = logging.getLogger(__name__)


class RetryPolicy:
    """Exponential backoff with jitter for transient faults."""

    def __init__(self, attempts=3, base_delay=0.1, max_delay=2.0, jitter=0.1, retry_on=(TimeoutError,)):
        self.attempts = attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.retry_on = retry_on

    def delay(self, attempt):
        backoff = min(self.max_delay, self.base_delay * (2 ** attempt))
        return backoff + random.uniform(0, self.jitter)

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(self.attempts):
                try:
                    return fn(*args, **kwargs)
                except self.retry_on as exc:
                    if attempt == self.attempts - 1:
                        raise
                    log.warning("attempt %d failed: %s", attempt + 1, exc)
                    time.sleep(self.delay(attempt))
        return wrapper


DEFAULT_POLICY = RetryPolicy()


def parse(raw):
    """'21.5' -> 21.5; anything else is a real fault and raises ValueError."""
    return float(raw)


@DEFAULT_POLICY
def _fetch():
    return link.fetch()


def read_value():
    """One temperature reading from the field sensor."""
    return parse(_fetch())
