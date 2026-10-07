def profile_response(conn, user_id):
    """The dict sent as JSON for GET /me, or None if there is no such user."""
    row = conn.execute("SELECT id, email, name, created FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None
