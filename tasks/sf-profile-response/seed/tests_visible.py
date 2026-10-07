from accounts.api import profile_response
from accounts.store import connect

me = profile_response(connect(), 1)
assert me["email"] == "ann@example.org" and me["name"] == "Ann", me
print("ok")
