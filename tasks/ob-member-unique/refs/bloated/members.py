import sqlite3
from dataclasses import dataclass


class MemberError(Exception):
    """Base class for member errors."""


class DuplicateMemberError(MemberError):
    """Raised when an email address is already registered."""


class InvalidMemberError(MemberError):
    """Raised when a member record is not valid."""


@dataclass(frozen=True)
class Member:
    email: str
    name: str

    def normalised_email(self):
        return self.email.strip().lower()


class MemberRepository:
    """Data access for the members table."""

    def __init__(self, conn):
        self.conn = conn

    def exists(self, email):
        row = self.conn.execute("SELECT 1 FROM members WHERE lower(email) = ?", (email,)).fetchone()
        return row is not None

    def insert(self, member):
        self.conn.execute("INSERT INTO members (email, name) VALUES (?, ?)",
                          (member.email.strip(), member.name.strip()))


class MemberService:
    """Business rules for registering members."""

    def __init__(self, conn):
        self.repository = MemberRepository(conn)
        self.conn = conn

    def validate(self, member):
        if "@" not in member.email:
            raise InvalidMemberError(f"not an email: {member.email}")

    def register(self, member):
        self.validate(member)
        if self.repository.exists(member.normalised_email()):
            raise DuplicateMemberError(f"{member.email} is already a member")
        self.repository.insert(member)


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS members ("
        " id INTEGER PRIMARY KEY,"
        " email TEXT NOT NULL,"
        " name TEXT NOT NULL)"
    )
    return conn


def add_member(conn, email, name):
    """Register one member from the sign-up form."""
    MemberService(conn).register(Member(email, name))
    conn.commit()


def import_members(conn, rows):
    """Bulk import from the old system: rows of (email, name)."""
    service = MemberService(conn)
    for email, name in rows:
        service.register(Member(email, name))
    conn.commit()


def count(conn):
    return conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
