from accounts.auth import Auth

auth = Auth()
auth.register("ann", "correct horse battery")
token = auth.login("ann", "correct horse battery")
assert auth.user_for(token) == "ann"
print("ok")
