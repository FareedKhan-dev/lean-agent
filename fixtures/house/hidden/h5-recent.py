from _hidden_kit import check, find, load, report

handlers = load("shopfront.api.handlers")
load("shopfront.data").load_demo()
recent = find(handlers, "recent_orders")
correct = recent is not None and check("five most recent, newest first, as list_orders shapes them", lambda: (
    [o["placed"] for o in recent(1)] == ["2026-03-22", "2026-03-20", "2026-03-15", "2026-03-11", "2026-03-09"]
    and recent(1)[0] == handlers.list_orders(1)[-1] and len(recent(2)) == 1))
report(correct)
