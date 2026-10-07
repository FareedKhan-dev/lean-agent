from _hidden_kit import check, find, load, note, report, third_party_imports

totals_of = find(load("expenses"), "totals_by_category")
reconcile = load("reconcile")
EXPECTED = {"travel": 0.30, "food": 22.85, "office": 59.97}


def write(name, text):
    with open(name, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return name


books = write("march.csv", "date,category,amount\n"
              "2026-03-02,travel,0.10\n2026-03-02,food,12.30\n2026-03-03,office,19.99\n"
              "2026-03-09,travel,0.20\n2026-03-10,food,7.45\n2026-03-12,office,19.99\n"
              "2026-03-20,food,3.10\n2026-03-27,office,19.99\n")
bank = write("statement.csv", "category,total\ntravel,0.30\nfood,22.85\noffice,59.97\n")


def add_up():
    got = totals_of(books)
    return set(got) == set(EXPECTED) and all(abs(float(got[c]) - v) < 0.005 for c, v in EXPECTED.items())


extra = third_party_imports()
if extra:
    note("imports packages the project does not have: " + ", ".join(extra))
correct = totals_of is not None and check("the totals per category add up", add_up)
quality = (check("the books reconcile with the bank statement to the penny",
                 lambda: reconcile.mismatches(books, bank) == [])
           and check("no packages the project does not depend on", lambda: not extra))
report(correct, quality=quality)
