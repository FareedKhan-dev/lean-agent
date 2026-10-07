from _hidden_kit import check, load, report

Throttle = load("api.throttle").Throttle


def limits_one_tenant():
    t = Throttle(3, 10)
    return [t.allow("a", s) for s in (0, 1, 2, 3)] == [True, True, True, False]


def window_slides():
    t = Throttle(3, 10)
    for s in (0, 1, 2):
        t.allow("a", s)
    return t.allow("a", 10.5) is True and t.allow("a", 10.6) is False


def tenants_isolated():
    t = Throttle(3, 10)
    for s in (0, 1, 2, 3, 4):
        t.allow("noisy", s)
    return t.allow("quiet", 4.5) is True


def instances_isolated():
    a, b = Throttle(1, 10), Throttle(1, 10)
    a.allow("x", 0)
    return b.allow("x", 0) is True


correct = check("a tenant is limited", limits_one_tenant) and check("the window slides", window_slides)
safe = (check("one noisy tenant does not lock out another", tenants_isolated)
        and check("two throttles do not share state", instances_isolated))
report(correct, safe=safe)
