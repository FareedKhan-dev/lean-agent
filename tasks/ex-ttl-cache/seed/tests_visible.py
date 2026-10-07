from cache import TTLCache

c = TTLCache(max_size=2, ttl=60)
c.set("kettle", 2499)
assert c.get("kettle") == 2499 and c.get("toaster") is None
print("ok")
