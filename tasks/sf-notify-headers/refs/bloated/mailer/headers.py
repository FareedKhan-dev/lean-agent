from dataclasses import dataclass


class HeaderError(ValueError):
    pass


@dataclass(frozen=True)
class Header:
    name: str
    value: str

    def validate(self):
        if any(ch in self.value for ch in "\r\n"):
            raise HeaderError(f"{self.name} cannot contain line breaks")
        if not self.name.replace("-", "").isalnum():
            raise HeaderError(f"bad header name: {self.name}")
        return self

    def render(self):
        return f"{self.name}: {self.value}\r\n"


class HeaderBlock:
    def __init__(self):
        self.headers = []

    def add(self, name, value):
        self.headers.append(Header(name, value).validate())
        return self

    def render(self):
        return "".join(h.render() for h in self.headers)


def build_headers(to, subject):
    """'To: <to>\\r\\nSubject: <subject>\\r\\n'"""
    return HeaderBlock().add("To", to).add("Subject", subject).render()
