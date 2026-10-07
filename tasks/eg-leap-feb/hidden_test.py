import datetime

from _hidden_kit import check, find, load, report

add = find(load("leases.dates"), "add_months")
schedule = load("leases.schedule")
D = datetime.date

ORDINARY = [  # (start, months, expected)
    (D(2026, 3, 15), 1, D(2026, 4, 15)), (D(2026, 3, 15), 0, D(2026, 3, 15)),
    (D(2026, 12, 15), 1, D(2027, 1, 15)), (D(2026, 11, 30), 3, D(2027, 2, 28)),
    (D(2026, 8, 31), 1, D(2026, 9, 30)), (D(2026, 1, 31), 2, D(2026, 3, 31)),
]
LEAP = [
    (D(2026, 1, 31), 1, D(2026, 2, 28)), (D(2024, 1, 31), 1, D(2024, 2, 29)),
    (D(2000, 1, 31), 1, D(2000, 2, 29)), (D(1900, 1, 31), 1, D(1900, 2, 28)),
    (D(2100, 1, 31), 1, D(2100, 2, 28)), (D(2024, 2, 29), 12, D(2025, 2, 28)),
    (D(1891, 3, 25), 999 * 12, D(2890, 3, 25)),
]


def all_match(cases):
    for start, months, want in cases:
        got = add(start, months)
        assert got == want, f"{start} plus {months} months gave {got}, not {want}"
    return True


correct = add is not None and all([
    check("ordinary months, year ends and short months", lambda: all_match(ORDINARY)),
    check("February in leap and common years, 1900 and 2100 included", lambda: all_match(LEAP)),
    check("the schedule's first payment and lease end",
          lambda: schedule.first_payment({"start": D(2028, 1, 31), "years": 1}) == D(2028, 2, 29)
          and schedule.lease_end({"start": D(2028, 2, 29), "years": 72}) == D(2100, 2, 28))])
report(correct)
