from notify import gateway


def send_all(numbers, message):
    """Text `message` to every number in `numbers` (a list)."""
    gateway.send(numbers, message)
