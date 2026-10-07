from shop.pages import page_count, page_items


def render_listing(products, page, per_page=10):
    pages = page_count(len(products), per_page)
    if not 1 <= page <= pages:
        return "no such page"
    return f"page {page} of {pages}: " + ", ".join(page_items(products, page, per_page))
