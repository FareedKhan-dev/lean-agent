import os
import re
import unicodedata


class Step:
    def apply(self, name):
        raise NotImplementedError


class Normalise(Step):
    def apply(self, name):
        return unicodedata.normalize("NFKC", name)


class DropDirectories(Step):
    def apply(self, name):
        return name.replace("\\", "/").split("/")[-1]


class ReplaceUnsafe(Step):
    def apply(self, name):
        return re.sub(r"[^\w.\-]+", "_", name).strip("._") or "file"


class GuardReserved(Step):
    RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}

    def apply(self, name):
        return "_" + name if name.partition(".")[0].upper() in self.RESERVED else name


class Truncate(Step):
    def __init__(self, limit=80):
        self.limit = limit

    def apply(self, name):
        return name[:self.limit]


class FilenameSanitiser:
    def __init__(self, steps=None):
        self.steps = steps or [Normalise(), DropDirectories(), ReplaceUnsafe(), GuardReserved(), Truncate()]

    def clean(self, name):
        for step in self.steps:
            name = step.apply(name)
        return name


def attachment_path(folder, filename):
    """Where an incoming attachment is saved: a file inside `folder`."""
    return os.path.join(folder, FilenameSanitiser().clean(filename))
