from itertools import batched


def batches(items, size):
    """Consecutive batches of `size` items from `items`; the last one may be shorter."""
    return batched(items, size)
