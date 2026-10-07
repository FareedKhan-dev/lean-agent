from decimal import Decimal

from invoicing.checks import is_balanced
from invoicing.exporters import export
from invoicing.models import Invoice, Line
from invoicing.totals import invoice_total


def test_total():
    invoice = Invoice("A-1", "Ann", "2026-03-02", [Line("kettle", 1, 1000)])
    assert invoice_total(invoice) == Decimal("12")
    assert is_balanced(invoice)


def test_csv_export():
    invoice = Invoice("A-2", "Bo", "2026-03-03", [])
    assert export(invoice, "csv") == "A-2,Bo"


if __name__ == "__main__":
    test_total()
    test_csv_export()
    print("ok")
