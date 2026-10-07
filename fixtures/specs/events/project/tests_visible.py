from events.dispatcher import Dispatcher

d = Dispatcher()
seen = []
d.subscribe("order.placed", seen.append)
assert d.publish("order.placed", {"id": 1}) == 1 and seen == [{"id": 1}]
print("ok")
