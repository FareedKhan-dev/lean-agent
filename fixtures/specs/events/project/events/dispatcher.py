class DeliveryError(Exception):
    """Raised by publish after every handler has run, if any of them failed."""


class Dispatcher:
    """See SPEC.md."""
