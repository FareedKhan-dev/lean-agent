from dataclasses import dataclass
from itertools import islice


@dataclass(frozen=True)
class BatchPolicy:
    size: int

    def __post_init__(self):
        if self.size < 1:
            raise ValueError("size must be at least 1")


class Batcher:
    """Splits any iterable into lists of at most `policy.size` items, lazily."""

    def __init__(self, policy):
        self.policy = policy
        self.batches_made = 0

    def split(self, items):
        it = iter(items)
        while batch := list(islice(it, self.policy.size)):
            self.batches_made += 1
            yield batch


def batches(items, size):
    """Consecutive batches of `size` items from `items`; the last one may be shorter."""
    return Batcher(BatchPolicy(size)).split(items)
