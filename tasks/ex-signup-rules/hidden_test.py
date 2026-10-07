from _hidden_kit import check, find, load, report

validate = find(load("signup"), "validate_signup")
views = load("views")
GOOD = {"username": "ann_k", "email": "ann@example.org", "password": "correct horse 42", "age": "34"}
M = ["username must be 3 to 20 characters", "username may only use letters, digits and _",
     "email address is not valid", "password must be at least 12 characters",
     "password needs a letter and a digit", "password must not contain the username",
     "age must be a whole number from 13 to 120"]
CASES = [  # (changes to a good form, the messages that must come back)
    ({}, []), ({"age": ""}, []), ({"age": "13"}, []), ({"age": "120"}, []),
    ({"username": "abc"}, []), ({"username": "a" * 20}, []), ({"password": "abcdefghij12"}, []),
    ({"email": "a@b.co"}, []), ({"email": "a@bc.d"}, []),
    ({"username": "al"}, [M[0]]), ({"username": "a" * 21}, [M[0]]),
    ({"username": "ann k!"}, [M[1]]), ({"username": "anné"}, [M[1]]),
    ({"email": "ann.example.org"}, [M[2]]), ({"email": "ann@@example.org"}, [M[2]]),
    ({"email": "@example.org"}, [M[2]]), ({"email": "ann@example"}, [M[2]]),
    ({"email": "ann@.org"}, [M[2]]), ({"email": "ann@example."}, [M[2]]),
    ({"password": "short 42"}, [M[3]]), ({"password": "no digits at all"}, [M[4]]),
    ({"password": "1234567890123"}, [M[4]]), ({"password": "my ANN_K pass 42"}, [M[5]]),
    ({"age": "12"}, [M[6]]), ({"age": "121"}, [M[6]]), ({"age": "thirty"}, [M[6]]), ({"age": "13.5"}, [M[6]]),
]


def each_rule_alone():
    for changes, want in CASES:
        got = validate({**GOOD, **changes})
        assert got == want, f"{changes} gave {got}"
    return True


correct = validate is not None and all([
    check("each rule fires on its own, with its own message", each_rule_alone),
    check("every failing rule is reported, in order",
          lambda: validate({"username": "a!", "email": "nope", "password": "a!", "age": "7"}) == M),
    check("missing fields count as empty", lambda: validate({}) == [M[0], M[2], M[3], M[4]]),
    check("the sign-up view answers 400 with the messages",
          lambda: views.post_signup({**GOOD, "age": "12"}) == (400, {"errors": [M[6]]})
          and views.post_signup(GOOD) == (201, {"welcome": "ann_k"}))])
report(correct)
