import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    number: int
    items: list
    total_pages: int

    @property
    def has_next(self):
        return self.number < self.total_pages

    @property
    def has_previous(self):
        return self.number > 1


class Paginator:
    def __init__(self, items, per_page):
        if per_page < 1:
            raise ValueError("per_page must be at least 1")
        self.items = items
        self.per_page = per_page

    @property
    def total_pages(self):
        return math.ceil(len(self.items) / self.per_page)

    def page(self, number):
        start = (number - 1) * self.per_page
        return Page(number, self.items[start:start + self.per_page], self.total_pages)


def page_count(total, per_page):
    """How many pages it takes to show `total` items, `per_page` to a page."""
    return Paginator(range(total), per_page).total_pages


def page_items(items, page, per_page):
    """The items on page `page`, counting from 1."""
    return Paginator(items, per_page).page(page).items
