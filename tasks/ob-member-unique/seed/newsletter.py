def recipients(conn):
    return [row[0] for row in conn.execute("SELECT email FROM members ORDER BY id")]
