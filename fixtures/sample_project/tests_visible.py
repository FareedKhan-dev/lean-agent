import datetime

from library.catalogue import overdue
from library.loans import due_date, fine

D = datetime.date
assert due_date(D(2026, 3, 1)) == D(2026, 3, 15)
assert fine(D(2026, 3, 1), D(2026, 3, 10)) == 0
assert overdue([("Emma", D(2026, 3, 1))], D(2026, 3, 5)) == []
print("visible tests passed")
