"""Client for the SMS gateway. The gateway refuses more than 50 numbers per request."""
REQUESTS = []
LIMIT = 50


def send(numbers, message):
    if len(numbers) > LIMIT:
        raise ValueError(f"gateway refused {len(numbers)} numbers (limit {LIMIT})")
    REQUESTS.append((list(numbers), message))
