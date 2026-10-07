from api.throttle import Throttle

t = Throttle(limit=2, window_s=10)
assert t.allow("acme", 0) and t.allow("acme", 1) and not t.allow("acme", 2)
print("ok")
