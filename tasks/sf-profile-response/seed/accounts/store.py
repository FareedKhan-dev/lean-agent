import sqlite3

USERS = [
    (1, "ann@example.org", "Ann", "pbkdf2$600000$c2FsdA$aGFzaGE", "ak-demo-7f3a9c", "2026-01-04"),
    (2, "bo@example.org", "Bo", "pbkdf2$600000$c2FsdB$aGFzaGI", "ak-demo-2b8e1d", "2026-02-11"),
]


def connect():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, name TEXT, "
                 "password_hash TEXT, api_key TEXT, created TEXT)")
    conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", USERS)
    return conn
