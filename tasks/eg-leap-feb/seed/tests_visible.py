import datetime

from leases.dates import add_months

assert add_months(datetime.date(2026, 3, 15), 1) == datetime.date(2026, 4, 15)
print("ok")
