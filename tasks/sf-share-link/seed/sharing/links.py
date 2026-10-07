import hashlib
import hmac


def _sign(payload, secret):
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def make_link(doc_id, expires_at, secret):
    """A share token '<doc_id>.<expires_at>.<signature>'; expires_at is a Unix time."""
    payload = f"{doc_id}.{int(expires_at)}"
    return f"{payload}.{_sign(payload, secret)}"


def open_link(token, secret, now):
    """Return the document id this token grants access to, or None if it is not valid."""
    raise NotImplementedError
