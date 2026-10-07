from _hidden_kit import check, code_lines_added, load, note, report

pages = load("shop.pages")
listing = load("shop.listing")
lamps = [f"lamp {i}" for i in range(1, 26)]

added = code_lines_added()
note(f"lines of code added: {added}")
correct = all([
    check("page counts round up", lambda: [pages.page_count(n, 10) for n in (25, 1, 9, 11)] == [3, 1, 1, 2]),
    check("an exact fit has no empty extra page", lambda: [pages.page_count(n, 10) for n in (10, 20, 30)] == [1, 2, 3]),
    check("the last page shows the last products",
          lambda: listing.render_listing(lamps, 3) == "page 3 of 3: lamp 21, lamp 22, lamp 23, lamp 24, lamp 25"),
    check("there is no page after the last", lambda: listing.render_listing(lamps, 4) == "no such page")])
quality = check("the fix stays small: at most two lines of code", lambda: added <= 2)
report(correct, quality=quality)
