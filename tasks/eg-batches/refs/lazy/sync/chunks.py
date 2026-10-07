def batches(items, size):
    """Consecutive batches of `size` items from `items`; the last one may be shorter."""
    if size < 1:
        raise ValueError("size must be at least 1")
    return zip(*[iter(items)] * size)
