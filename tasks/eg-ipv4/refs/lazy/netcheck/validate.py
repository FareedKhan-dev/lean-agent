import re


def is_ipv4(text):
    """True if `text` is an IPv4 address in dotted form, like 192.168.0.1."""
    return re.match(r"^(\d{1,3}\.){3}\d{1,3}$", text) is not None
