import string
from abc import ABC, abstractmethod

RULES = []


def rule(cls):
    """Class decorator: register a rule, in the order the rules are defined."""
    RULES.append(cls())
    return cls


class Rule(ABC):
    message = ""

    @abstractmethod
    def passes(self, form):
        ...

    def check(self, form):
        return None if self.passes(form) else self.message


class FormView:
    """Read access to the posted form, where a missing field reads as empty."""

    def __init__(self, form):
        self.form = form

    def __getitem__(self, name):
        return self.form.get(name, "")


@rule
class UsernameLength(Rule):
    message = "username must be 3 to 20 characters"

    def passes(self, form):
        return 3 <= len(form["username"]) <= 20


@rule
class UsernameCharacters(Rule):
    message = "username may only use letters, digits and _"
    allowed = set(string.ascii_letters + string.digits + "_")

    def passes(self, form):
        return set(form["username"]) <= self.allowed


@rule
class EmailShape(Rule):
    message = "email address is not valid"

    def passes(self, form):
        local, at, domain = form["email"].partition("@")
        return bool(at and local) and "@" not in domain and "." in domain[1:-1]


@rule
class PasswordLength(Rule):
    message = "password must be at least 12 characters"

    def passes(self, form):
        return len(form["password"]) >= 12


@rule
class PasswordMix(Rule):
    message = "password needs a letter and a digit"

    def passes(self, form):
        password = form["password"]
        return any(c.isalpha() for c in password) and any(c.isdigit() for c in password)


@rule
class PasswordNotUsername(Rule):
    message = "password must not contain the username"

    def passes(self, form):
        return not form["username"] or form["username"].casefold() not in form["password"].casefold()


@rule
class AgeRange(Rule):
    message = "age must be a whole number from 13 to 120"

    def passes(self, form):
        age = form["age"]
        return not age or (age.isdecimal() and 13 <= int(age) <= 120)


class SignupValidator:
    def __init__(self, rules=None):
        self.rules = rules if rules is not None else RULES

    def validate(self, form):
        view = FormView(form)
        return [m for m in (r.check(view) for r in self.rules) if m]


def validate_signup(form):
    """The sign-up form's error messages, in rule order; an empty list if the form is fine."""
    return SignupValidator().validate(form)
