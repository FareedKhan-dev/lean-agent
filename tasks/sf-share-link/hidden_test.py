from _hidden_kit import check, load, report

links = load("sharing.links")
SECRET, NOW = "s3cret", 1_900_000_000
token = links.make_link("doc42", NOW + 3600, SECRET)
doc, expires, sig = token.rsplit(".", 2)


def rejected(text, now=NOW):
    try:
        return links.open_link(text, SECRET, now) is None
    except ValueError:
        return True


correct = (check("a valid link opens its document", lambda: links.open_link(token, SECRET, NOW) == "doc42")
           and check("a document id with a dot in it still opens",
                     lambda: links.open_link(links.make_link("q3.report", NOW + 3600, SECRET), SECRET, NOW) == "q3.report"))
safe = (check("a link for another document is refused", lambda: rejected(f"doc43.{expires}.{sig}"))
        and check("a link with a longer expiry is refused", lambda: rejected(f"{doc}.{int(expires) + 999999}.{sig}"))
        and check("an expired link is refused", lambda: rejected(token, now=NOW + 7200))
        and check("a link signed with another secret is refused",
                  lambda: rejected(links.make_link("doc42", NOW + 3600, "other")))
        and check("garbage is refused, not a crash", lambda: rejected("garbage") and rejected("a.b.c.d")))
report(correct, safe=safe)
