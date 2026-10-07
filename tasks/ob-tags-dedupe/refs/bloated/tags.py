import unicodedata
from abc import ABC, abstractmethod


class NormalisationStep(ABC):
    @abstractmethod
    def apply(self, text):
        ...


class UnicodeNormalise(NormalisationStep):
    def __init__(self, form="NFC"):
        self.form = form

    def apply(self, text):
        return unicodedata.normalize(self.form, text)


class CaseFold(NormalisationStep):
    def apply(self, text):
        return text.casefold()


class TagNormaliser:
    """Builds the comparison key for a tag from a configurable list of steps."""

    def __init__(self, steps=None):
        self.steps = steps if steps is not None else [UnicodeNormalise(), CaseFold()]

    def key(self, tag):
        for step in self.steps:
            tag = step.apply(tag)
        return tag


class TagSet:
    def __init__(self, normaliser=None):
        self.normaliser = normaliser or TagNormaliser()
        self._items = {}

    def add(self, tag):
        self._items.setdefault(self.normaliser.key(tag), tag)

    def __iter__(self):
        return iter(self._items.values())


def unique_tags(tags):
    """The tags with repeats removed, ignoring case: the first spelling of each, in order."""
    tag_set = TagSet()
    for tag in tags:
        tag_set.add(tag)
    return list(tag_set)
