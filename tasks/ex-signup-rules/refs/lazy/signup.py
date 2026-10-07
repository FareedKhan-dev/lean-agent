import re

RULES = [
    (lambda f: 3 <= len(f.get("username", "")) <= 20, "username must be 3 to 20 characters"),
    (lambda f: re.fullmatch(r"\w*", f.get("username", ""), re.ASCII), "username may only use letters, digits and _"),
    (lambda f: re.fullmatch(r"[^@]+@[^@]+\.[^@]+", f.get("email", "")), "email address is not valid"),
    (lambda f: len(f.get("password", "")) >= 12, "password must be at least 12 characters"),
]


def validate_signup(form):
    """The sign-up form's error messages, in rule order; an empty list if the form is fine."""
    for ok, message in RULES:
        if not ok(form):
            return [message]
    return []
