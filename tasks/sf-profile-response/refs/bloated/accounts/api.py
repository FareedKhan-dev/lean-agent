from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProfileDTO:
    id: int
    email: str
    name: str
    created: str


class ProfileSerializer:
    """Turns a user row into the public profile, using an explicit field allowlist."""

    public_fields = ("id", "email", "name", "created")

    def serialise(self, row):
        return asdict(ProfileDTO(**{k: row[k] for k in self.public_fields}))


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def by_id(self, user_id):
        return self.conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def profile_response(conn, user_id):
    """The dict sent as JSON for GET /me, or None if there is no such user."""
    row = UserRepository(conn).by_id(user_id)
    return ProfileSerializer().serialise(row) if row else None
