def search_products(conn, term):
    """Names of products whose name contains `term`, ignoring case, sorted by name."""
    rows = conn.execute("SELECT name FROM products WHERE name LIKE ? ORDER BY name", (f"%{term}%",))
    return [name for (name,) in rows]
