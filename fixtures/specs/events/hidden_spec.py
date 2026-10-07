from _hidden_kit import check, load, raises, report

m = load("events.dispatcher")
D, DeliveryError = m.Dispatcher, m.DeliveryError


def order():
    d, calls = D(), []
    d.subscribe("t", lambda p: calls.append(("a", p)))
    d.subscribe("*", lambda p: calls.append(("star", p)))
    d.subscribe("t", lambda p: calls.append(("b", p)))
    n = d.publish("t", 1)
    return n == 3 and calls == [("a", 1), ("b", 1), ("star", 1)] and d.publish("other", 2) == 1


def unsubscribe():
    d, calls = D(), []
    sid = d.subscribe("t", calls.append)
    d.unsubscribe(sid)
    d.unsubscribe(12345)
    return d.publish("t", 1) == 0 and calls == []


def isolation():
    d, calls = D(), []
    bad = d.subscribe("t", lambda p: 1 / 0)
    d.subscribe("t", calls.append)
    try:
        d.publish("t", 7)
    except DeliveryError as e:
        return calls == [7] and len(e.errors) == 1 and e.errors[0][0] == bad and isinstance(e.errors[0][1], ZeroDivisionError)
    return False


def mutation_during_delivery():
    d, calls = D(), []
    def late(p):
        calls.append(("late", p))
    def first(p):
        calls.append(("first", p))
        d.subscribe("t", late)
    d.subscribe("t", first)
    d.publish("t", 1)
    d.publish("t", 2)
    return calls == [("first", 1), ("first", 2), ("late", 2)]


correct = all([check("handlers run in order, wildcard last, count returned", order),
               check("unsubscribe works and ignores unknown ids", unsubscribe),
               check("a failing handler does not stop the others", isolation),
               check("subscribing during delivery applies next time", mutation_during_delivery)])
report(correct)
