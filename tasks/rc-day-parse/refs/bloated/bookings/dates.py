import re
from datetime import date


class DateFormat:
    """One accepted way of writing a date."""

    def __init__(self, name, pattern):
        self.name = name
        self.pattern = re.compile(pattern)

    def parse(self, text):
        match = self.pattern.fullmatch(text)
        if not match:
            return None
        return date(int(match["y"]), int(match["m"]), int(match["d"]))


class DateParser:
    """Tries each registered format in order."""

    def __init__(self):
        self.formats = []

    def register(self, fmt):
        self.formats.append(fmt)
        return self

    def parse(self, text):
        text = text.strip()
        for fmt in self.formats:
            result = fmt.parse(text)
            if result is not None:
                return result
        raise ValueError(f"unrecognised date: {text!r}")


PARSER = (DateParser()
          .register(DateFormat("iso", r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})"))
          .register(DateFormat("unpadded", r"(?P<y>\d{4})-(?P<m>\d{1,2})-(?P<d>\d{1,2})")))


def parse_day(text):
    """'2026-03-07' -> date(2026, 3, 7)"""
    return PARSER.parse(text)
