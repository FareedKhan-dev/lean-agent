from _hidden_kit import check, load, report

m = load("events.dispatcher")


def once():
    d, calls = m.Dispatcher(), []
    d.subscribe("t", calls.append, once=True)
    d.subscribe("t", lambda p: calls.append(("always", p)))
    d.publish("t", 1)
    d.publish("t", 2)
    return calls == [1, ("always", 1), ("always", 2)]


correct = check("a once subscription is removed after one call", once)
report(correct)
