from itertools import batched

from notify import gateway


def send_all(numbers, message):
    """Text `message` to every number in `numbers` (a list), at most 50 per gateway request."""
    for group in batched(numbers, 50):
        gateway.send(list(group), message)
