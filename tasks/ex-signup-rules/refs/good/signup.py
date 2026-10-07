import string

USERNAME_CHARS = set(string.ascii_letters + string.digits + "_")


def _email_ok(email):
    local, at, domain = email.partition("@")
    return bool(at and local) and "@" not in domain and "." in domain[1:-1]


def validate_signup(form):
    """The sign-up form's error messages, in rule order; an empty list if the form is fine."""
    username, email = form.get("username", ""), form.get("email", "")
    password, age = form.get("password", ""), form.get("age", "")
    errors = []
    if not 3 <= len(username) <= 20:
        errors.append("username must be 3 to 20 characters")
    if not set(username) <= USERNAME_CHARS:
        errors.append("username may only use letters, digits and _")
    if not _email_ok(email):
        errors.append("email address is not valid")
    if len(password) < 12:
        errors.append("password must be at least 12 characters")
    if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        errors.append("password needs a letter and a digit")
    if username and username.casefold() in password.casefold():
        errors.append("password must not contain the username")
    if age and not (age.isdecimal() and 13 <= int(age) <= 120):
        errors.append("age must be a whole number from 13 to 120")
    return errors
