import sqlite3


def connect(rows):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE stock (sku TEXT, qty INTEGER)")
    conn.executemany("INSERT INTO stock VALUES (?, ?)", rows)
    return conn


def stock_rows(conn):
    """Every stock row, straight from the cursor: the table can be too big to load at once."""
    yield from conn.execute("SELECT sku, qty FROM stock ORDER BY sku")
