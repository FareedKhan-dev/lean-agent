from _hidden_kit import check, load, raises, report

Auth = load("accounts.auth").Auth
now = [1_000_000.0]
clock = lambda: now[0]
PW = "correct horse battery"


def fresh():
    now[0] = 1_000_000.0
    a = Auth(clock=clock)
    a.register("ann", PW)
    return a


def basics():
    a = fresh()
    t1, t2 = a.login("ann", PW), a.login("ann", PW)
    return a.user_for(t1) == "ann" and t1 != t2 and isinstance(t1, str) and len(t1) >= 16 and a.user_for("nope") is None


def no_plain_password():
    a = fresh()
    dump = repr(vars(a)) + "".join(repr(vars(v)) for v in vars(a).values() if hasattr(v, "__dict__"))
    return PW not in dump


def refusals():
    a = fresh()
    try:
        a.login("ann", "wrong password!")
    except PermissionError as e1:
        try:
            a.login("bob", PW)
        except PermissionError as e2:
            return str(e1) == str(e2) and raises(lambda: a.register("ann", "another password"), ValueError) \
                and raises(lambda: a.register("cy", "short"), ValueError)
    return False


def lockout():
    a = fresh()
    for _ in range(5):
        raises(lambda: a.login("ann", "wrong password!"), PermissionError)
    locked = raises(lambda: a.login("ann", PW), PermissionError)
    now[0] += 15 * 60 + 1
    return locked and a.user_for(a.login("ann", PW)) == "ann"


def expiry():
    a = fresh()
    t = a.login("ann", PW)
    now[0] += 3599
    alive = a.user_for(t) == "ann"
    now[0] += 2
    return alive and a.user_for(t) is None


correct = all([check("login gives a random token that maps back to the user", basics),
               check("the password is not stored as given", no_plain_password),
               check("wrong password and unknown user fail the same way; bad registrations refused", refusals),
               check("five failures lock the user out for 15 minutes", lockout),
               check("a token lasts one hour", expiry)])
report(correct)
