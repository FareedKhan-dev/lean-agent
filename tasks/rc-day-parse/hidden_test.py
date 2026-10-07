from datetime import date

from _hidden_kit import check, load, raises, report

window = load("bookings.window")
cancel = load("bookings.cancel")

correct = (check("the reported case works", lambda: window.booking_window("2026-3-7", "2026-3-9") == 2)
           and check("padded dates still work", lambda: window.booking_window("2026-03-07", "2026-03-10") == 3)
           and check("impossible dates still raise", lambda: raises(lambda: window.booking_window("2026-13-1", "2026-13-3"), ValueError)))
quality = (check("the cancellation deadline (never named in the report) accepts the same input",
                 lambda: cancel.cancel_deadline("2026-3-7") == date(2026, 3, 5))
           and check("and still rejects nonsense", lambda: raises(lambda: cancel.cancel_deadline("soon"), ValueError)))
report(correct, quality=quality)
