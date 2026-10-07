import sqlite3


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
    email = email.strip()
    taken = conn.execute("SELECT 1 FROM members WHERE lower(email) = lower(?)", (email,)).fetchone()
    if taken:
        raise ValueError(f"{email} is already a member")
    conn.execute("INSERT INTO members (email, name) VALUES (?, ?)", (email, name.strip()))
    conn.commit()


def import_members(conn, rows):
    """Bulk import from the old system: rows of (email, name)."""
    conn.executemany("INSERT INTO members (email, name) VALUES (?, ?)",
                     [(e.strip(), n.strip()) for e, n in rows])
    conn.commit()


def count(conn):
    return conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
