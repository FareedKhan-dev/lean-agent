import sqlite3

PRODUCTS = ["Desk lamp", "Lamp shade", "O'Brien armchair", "Oak table", "Reading lamp", "Rug"]


def connect():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price_pence INTEGER)")
    conn.executemany("INSERT INTO products (name, price_pence) VALUES (?, ?)",
                     [(name, 1000 + i * 250) for i, name in enumerate(PRODUCTS)])
    return conn
