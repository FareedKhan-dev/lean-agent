from signup import validate_signup

form = {"username": "ann_k", "email": "ann@example.org", "password": "correct horse 42", "age": "34"}
assert validate_signup(form) == [], validate_signup(form)
print("ok")
