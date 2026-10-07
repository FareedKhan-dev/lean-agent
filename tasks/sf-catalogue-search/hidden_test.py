from _hidden_kit import check, find, load, report

db = load("catalogue.db")
search = find(load("catalogue.search"), "search_products")
ALL = sorted(db.PRODUCTS)


def no_leak(term):
    try:
        got = search(db.connect(), term)
    except Exception:
        return False
    return got != ALL and all(name in ALL for name in got)


correct = search is not None and check("ordinary searches", lambda: (
    search(db.connect(), "lamp") == ["Desk lamp", "Lamp shade", "Reading lamp"]
    and search(db.connect(), "OAK") == ["Oak table"] and search(db.connect(), "zzz") == []))
safe = (check("an apostrophe in a real name works", lambda: search(db.connect(), "o'brien") == ["O'Brien armchair"])
        and check("a crafted term cannot list every product", lambda: no_leak("%' OR '1'='1"))
        and check("a crafted term cannot read other tables",
                  lambda: no_leak("' UNION SELECT name FROM sqlite_master --")))
report(correct, safe=safe)
