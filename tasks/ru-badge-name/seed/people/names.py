"""How a person's name is shown anywhere in the app. One place, so it is always the same."""

PARTICLES = {"van", "von", "de", "der", "den", "la", "le", "du", "da", "di", "del", "della", "ter", "ten"}


def _cap(part):
    return "'".join(p[:1].upper() + p[1:].lower() for p in part.split("'"))


def _word(word, first):
    if not first and word.lower() in PARTICLES:
        return word.lower()
    return "-".join(_cap(p) for p in word.split("-"))


def display_name(first, last):
    """'ludwig', 'VAN BEETHOVEN' -> 'Ludwig van Beethoven'; 'anne-marie', "o'neil" -> "Anne-Marie O'Neil"."""
    words = f"{first} {last}".split()
    return " ".join(_word(w, i == 0) for i, w in enumerate(words))
