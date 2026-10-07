from api.throttle import Throttle

THROTTLE = Throttle(limit=100, window_s=60)


def handle(tenant, now, path):
    if not THROTTLE.allow(tenant, now):
        return 429, "slow down"
    return 200, f"ok {path}"
