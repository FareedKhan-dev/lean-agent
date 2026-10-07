from _hidden_kit import check, load, raises, report

m = load("members")


def fresh():
    return m.connect(":memory:")


def duplicates(conn):
    return conn.execute("SELECT lower(email), COUNT(*) FROM members "
                        "GROUP BY lower(email) HAVING COUNT(*) > 1").fetchall()


def happy():
    c = fresh()
    m.add_member(c, "ann@example.org", "Ann")
    m.add_member(c, "bo@example.org", "Bo")
    return m.count(c) == 2


def add_rejects_case_duplicate():
    c = fresh()
    m.add_member(c, "Ann@Example.org", "Ann")
    return raises(lambda: m.add_member(c, "ann@example.org", "Ann again")) and not duplicates(c)


def import_cannot_duplicate():
    c = fresh()
    m.add_member(c, "ann@example.org", "Ann")
    try:
        m.import_members(c, [("ANN@example.org", "Ann"), ("cy@example.org", "Cy")])
    except Exception:
        pass
    return not duplicates(c)


def import_within_one_batch():
    c = fresh()
    try:
        m.import_members(c, [("dee@example.org", "Dee"), ("Dee@Example.org", "Dee 2")])
    except Exception:
        pass
    return not duplicates(c)


correct = (check("members can still be added", happy)
           and check("adding a different-case duplicate raises", add_rejects_case_duplicate))
quality = (check("the bulk import cannot create a duplicate", import_cannot_duplicate)
           and check("duplicates inside one import are refused", import_within_one_batch))
report(correct, quality=quality)
