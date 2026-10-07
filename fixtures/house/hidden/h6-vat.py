from _hidden_kit import check, load, report

models = load("shopfront.models.order")
Order, Line = models.Order, models.OrderLine
correct = check("totals with VAT, halves rounded up", lambda: (
    Order(1, 1, "2026-03-01", [Line("a", 1, 1000)]).total_with_vat() == 1200
    and Order(2, 1, "2026-03-01", [Line("a", 1, 2499)]).total_with_vat() == 2999
    and Order(3, 1, "2026-03-01", [Line("a", 1, 5)]).total_with_vat() == 6
    and isinstance(Order(4, 1, "2026-03-01", [Line("a", 1, 999)]).total_with_vat(), int)))
report(correct)
