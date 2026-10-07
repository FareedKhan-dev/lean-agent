import hashlib
import hmac
import secrets
import time

LOCK_AFTER, LOCK_SECONDS, TOKEN_SECONDS, ROUNDS = 5, 15 * 60, 60 * 60, 200_000


class Auth:
    """See SPEC.md."""

    def __init__(self, clock=time.time):
        self.clock = clock
        self._users, self._tokens, self._failures = {}, {}, {}

    def _hash(self, password, salt):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ROUNDS)

    def register(self, username, password):
        if username in self._users:
            raise ValueError("that username is taken")
        if len(password) < 10:
            raise ValueError("passwords need at least 10 characters")
        salt = secrets.token_bytes(16)
        self._users[username] = (salt, self._hash(password, salt))

    def login(self, username, password):
        count, since = self._failures.get(username, (0, 0.0))
        if count >= LOCK_AFTER and self.clock() - since < LOCK_SECONDS:
            raise PermissionError("too many failed attempts; try again later")
        user = self._users.get(username)
        if user is None or not hmac.compare_digest(self._hash(password, user[0]), user[1]):
            self._failures[username] = (count + 1, self.clock())
            raise PermissionError("wrong username or password")
        self._failures.pop(username, None)
        token = secrets.token_urlsafe(24)
        self._tokens[token] = (username, self.clock() + TOKEN_SECONDS)
        return token

    def user_for(self, token):
        username, expires = self._tokens.get(token, (None, 0.0))
        return username if self.clock() < expires else None

    def logout(self, token):
        self._tokens.pop(token, None)
