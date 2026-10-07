def export_all(conn):
    """Full table export for the internal admin tool (staff only)."""
    return [dict(row) for row in conn.execute("SELECT * FROM users")]
