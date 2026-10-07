import time


def _deliver(text, outbox):
    outbox.append(text)


def send(text, outbox, attempts=3):
    """Send an invoice, retrying in case delivery fails."""
    for attempt in range(attempts):
        try:
            return _deliver(text, outbox)
        except Exception:
            time.sleep(0.1 * 2 ** attempt)
    raise RuntimeError("could not send the invoice")
