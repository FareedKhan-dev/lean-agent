from _hidden_kit import check, load, newer_than_39, note, report, workspace_py

gateway = load("notify.gateway")
sms = load("notify.sms")


def sent(count):
    gateway.REQUESTS.clear()
    numbers = [f"07700{i:06d}" for i in range(count)]
    sms.send_all(numbers, "Ferry cancelled")
    flat = [n for group, _ in gateway.REQUESTS for n in group]
    return [len(group) for group, _ in gateway.REQUESTS], flat == numbers


too_new = newer_than_39(workspace_py())
if too_new:
    note("needs a newer Python than the project declares: " + ", ".join(too_new))
correct = all([
    check("120 numbers go out as 50, 50 and 20, each once and in order", lambda: sent(120) == ([50, 50, 20], True)),
    check("exactly 50 is one request", lambda: sent(50) == ([50], True)),
    check("a short list is one request", lambda: sent(3) == ([3], True)),
    check("the message reaches the gateway", lambda: sent(1) and gateway.REQUESTS[0][1] == "Ferry cancelled")])
quality = check("runs on the Python the project declares (3.9)", lambda: not too_new)
report(correct, quality=quality)
