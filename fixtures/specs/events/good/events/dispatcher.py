import itertools


class DeliveryError(Exception):
    """Raised by publish after every handler has run, if any of them failed."""

    def __init__(self, errors):
        super().__init__(f"{len(errors)} handler(s) failed")
        self.errors = errors


class Dispatcher:
    """See SPEC.md."""

    def __init__(self):
        self._subs = {}                    # id -> (topic, handler), in subscription order
        self._ids = itertools.count(1)

    def subscribe(self, topic, handler):
        sid = next(self._ids)
        self._subs[sid] = (topic, handler)
        return sid

    def unsubscribe(self, subscription_id):
        self._subs.pop(subscription_id, None)

    def publish(self, topic, payload):
        targets = [(sid, h) for sid, (t, h) in self._subs.items() if t == topic]
        targets += [(sid, h) for sid, (t, h) in self._subs.items() if t == "*"]
        errors = []
        for sid, handler in targets:
            try:
                handler(payload)
            except Exception as e:
                errors.append((sid, e))
        if errors:
            raise DeliveryError(errors)
        return len(targets)
