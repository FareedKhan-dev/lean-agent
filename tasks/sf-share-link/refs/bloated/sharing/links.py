import hashlib
import hmac
from dataclasses import dataclass


@dataclass(frozen=True)
class ShareToken:
    doc_id: str
    expires_at: int
    signature: str

    @property
    def payload(self):
        return f"{self.doc_id}.{self.expires_at}"


class TokenCodec:
    separator = "."

    def encode(self, token):
        return self.separator.join([token.doc_id, str(token.expires_at), token.signature])

    def decode(self, text):
        doc_id, expires_at, signature = text.rsplit(self.separator, 2)
        return ShareToken(doc_id, int(expires_at), signature)


class Signer:
    def __init__(self, secret, digest=hashlib.sha256):
        self.secret = secret.encode()
        self.digest = digest

    def sign(self, payload):
        return hmac.new(self.secret, payload.encode(), self.digest).hexdigest()

    def verify(self, payload, signature):
        return hmac.compare_digest(signature, self.sign(payload))


class ShareLinkService:
    def __init__(self, secret, codec=None):
        self.signer = Signer(secret)
        self.codec = codec or TokenCodec()

    def create(self, doc_id, expires_at):
        token = ShareToken(doc_id, int(expires_at), "")
        return self.codec.encode(ShareToken(doc_id, int(expires_at), self.signer.sign(token.payload)))

    def open(self, text, now):
        try:
            token = self.codec.decode(text)
        except ValueError:
            return None
        if not self.signer.verify(token.payload, token.signature) or now >= token.expires_at:
            return None
        return token.doc_id


def _sign(payload, secret):
    return Signer(secret).sign(payload)


def make_link(doc_id, expires_at, secret):
    """A share token '<doc_id>.<expires_at>.<signature>'; expires_at is a Unix time."""
    return ShareLinkService(secret).create(doc_id, expires_at)


def open_link(token, secret, now):
    """Return the document id this token grants access to, or None if it is not valid."""
    return ShareLinkService(secret).open(token, now)
