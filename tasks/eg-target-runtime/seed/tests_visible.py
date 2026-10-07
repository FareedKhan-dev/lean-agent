from notify import gateway, sms

sms.send_all([f"07700900{i:03d}" for i in range(120)], "Ferry cancelled")
assert [len(n) for n, _ in gateway.REQUESTS] == [50, 50, 20], gateway.REQUESTS
print("ok")
