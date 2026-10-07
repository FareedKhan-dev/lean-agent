"""Conference badges."""
from dataclasses import dataclass


class NameFormatter:
    """Formats personal names for printing."""

    PARTICLES = {"van", "von", "de", "der", "den", "la", "le", "du", "da", "di", "del", "della", "ter", "ten"}

    def capitalise(self, part):
        return "'".join(p[:1].upper() + p[1:].lower() for p in part.split("'"))

    def word(self, word, first):
        if not first and word.lower() in self.PARTICLES:
            return word.lower()
        return "-".join(self.capitalise(p) for p in word.split("-"))

    def format(self, first, last):
        words = f"{first} {last}".split()
        return " ".join(self.word(w, i == 0) for i, w in enumerate(words))


@dataclass(frozen=True)
class Badge:
    first: str
    last: str
    company: str

    def render(self, formatter=None):
        formatter = formatter or NameFormatter()
        return f"{formatter.format(self.first, self.last)} - {self.company}"


def badge_text(first, last, company):
    """The line printed on a badge, e.g. 'Ada Lovelace - Analytical Engines'."""
    return Badge(first, last, company).render()
