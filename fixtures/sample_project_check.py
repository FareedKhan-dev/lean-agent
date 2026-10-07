"""Our check for the S94b demo, never shown to the agent: a book returned on its due date is
not late, anywhere the library asks."""
import datetime

from library.catalogue import overdue
from library.loans import fine

D = datetime.date
assert fine(D(2026, 3, 1), D(2026, 3, 15)) == 0, "fined on the due date"
assert fine(D(2026, 3, 1), D(2026, 3, 16)) == 20, "one day late should cost one day's fine"
assert overdue([("Emma", D(2026, 3, 1))], D(2026, 3, 15)) == [], "listed as overdue on its due date"
assert overdue([("Emma", D(2026, 3, 1))], D(2026, 3, 17)) == [("Emma", 2)], "two days late"
print("sample check passed")
