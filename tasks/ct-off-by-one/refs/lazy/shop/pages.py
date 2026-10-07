def page_count(total, per_page):
    """How many pages it takes to show `total` items, `per_page` to a page."""
    return total // per_page + 1


def page_items(items, page, per_page):
    """The items on page `page`, counting from 1."""
    start = (page - 1) * per_page
    return items[start:start + per_page]
