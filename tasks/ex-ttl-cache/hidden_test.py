from _hidden_kit import check, load, report

TTLCache = getattr(load("cache"), "TTLCache", None)
now = [0.0]


def make(max_size, ttl):
    now[0] = 0.0
    return TTLCache(max_size=max_size, ttl=ttl, clock=lambda: now[0])


def basics():
    c = make(3, 10)
    c.set("a", 1)
    return c.get("a") == 1 and c.get("zz") is None and c.get("zz", 0) == 0


def expires():
    c = make(3, 10)
    c.set("a", 1)
    now[0] = 9.0
    alive = c.get("a") == 1
    now[0] = 11.0
    return alive and c.get("a") is None


def set_again_restarts_the_clock():
    c = make(3, 10)
    c.set("a", 1)
    now[0] = 8.0
    c.set("a", 2)
    now[0] = 15.0
    return c.get("a") == 2


def least_recently_used_goes():
    c = make(2, 100)
    c.set("a", 1)
    c.set("b", 2)
    c.get("a")
    c.set("c", 3)
    return c.get("b") is None and c.get("a") == 1 and c.get("c") == 3


def update_does_not_evict():
    c = make(2, 100)
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 10)
    return c.get("b") == 2 and c.get("a") == 10 and c.stats()["evictions"] == 0


def counts():
    c = make(2, 100)
    c.set("a", 1)
    c.get("a")
    c.get("x")
    c.set("b", 2)
    c.set("c", 3)
    s = c.stats()
    return (s["hits"], s["misses"], s["evictions"]) == (1, 1, 1)


def expired_read_is_a_miss():
    c = make(2, 10)
    c.set("a", 1)
    now[0] = 50.0
    c.get("a")
    s = c.stats()
    return s["hits"] == 0 and s["misses"] == 1


correct = TTLCache is not None and all([
    check("set and get", basics),
    check("an entry expires ttl seconds after it was set", expires),
    check("setting a key again restarts its clock", set_again_restarts_the_clock),
    check("the least recently used entry is evicted", least_recently_used_goes),
    check("updating a key never evicts", update_does_not_evict),
    check("stats count hits, misses and evictions", counts),
    check("reading an expired entry is a miss", expired_read_is_a_miss)])
report(correct)
