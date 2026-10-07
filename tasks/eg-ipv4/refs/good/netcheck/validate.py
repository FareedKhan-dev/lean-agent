import ipaddress


def is_ipv4(text):
    """True if `text` is an IPv4 address in dotted form, like 192.168.0.1."""
    try:
        ipaddress.IPv4Address(text)
    except ValueError:
        return False
    return True
