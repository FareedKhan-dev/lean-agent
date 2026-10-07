from netcheck.validate import is_ipv4

assert is_ipv4("192.168.0.1") and not is_ipv4("not an address")
print("ok")
