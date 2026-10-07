from notify import gateway


def send_all(numbers, message):
    """Text `message` to every number in `numbers` (a list), at most 50 per gateway request."""
    for start in range(0, len(numbers), gateway.LIMIT):
        gateway.send(numbers[start:start + gateway.LIMIT], message)
