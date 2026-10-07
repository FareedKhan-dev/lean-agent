from _hidden_kit import check, load, report

Auth = load("accounts.auth").Auth


def logout():
    a = Auth()
    a.register("ann", "correct horse battery")
    t = a.login("ann", "correct horse battery")
    a.logout(t)
    a.logout("unknown")
    return a.user_for(t) is None


correct = check("a logged-out token stops working", logout)
report(correct)
