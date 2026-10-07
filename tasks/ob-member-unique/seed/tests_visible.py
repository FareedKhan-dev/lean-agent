from members import add_member, connect, count

conn = connect()
add_member(conn, "ann@example.org", "Ann")
add_member(conn, "bo@example.org", "Bo")
assert count(conn) == 2
print("ok")
