import sqlite3


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS members ("
        " id INTEGER PRIMARY KEY,"
        " email TEXT NOT NULL UNIQUE COLLATE NOCASE,"
        " name TEXT NOT NULL)"
    )
    return conn


def add_member(conn, email, name):
    """Register one member from the sign-up form."""
    conn.execute("INSERT INTO members (email, name) VALUES (?, ?)", (email.strip(), name.strip()))
    conn.commit()


def import_members(conn, rows):
    """Bulk import from the old system: rows of (email, name)."""
    conn.executemany("INSERT INTO members (email, name) VALUES (?, ?)",
                     [(e.strip(), n.strip()) for e, n in rows])
    conn.commit()


def count(conn):
    return conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
