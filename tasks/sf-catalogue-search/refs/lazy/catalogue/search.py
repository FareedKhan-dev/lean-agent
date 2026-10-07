def search_products(conn, term):
    """Names of products whose name contains `term`, ignoring case, sorted by name."""
    rows = conn.execute(f"SELECT name FROM products WHERE name LIKE '%{term}%' ORDER BY name")
    return [name for (name,) in rows]
