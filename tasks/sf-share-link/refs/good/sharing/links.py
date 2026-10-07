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
    try:
        doc_id, expires_at, signature = token.rsplit(".", 2)
        expires = int(expires_at)
    except ValueError:
        return None
    if not hmac.compare_digest(signature, _sign(f"{doc_id}.{expires_at}", secret)):
        return None
    return doc_id if now < expires else None
