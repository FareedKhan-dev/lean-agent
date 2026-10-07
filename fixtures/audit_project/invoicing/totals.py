from decimal import Decimal

from invoicing.settings import SETTINGS


def round_half_up(value, places=2):
    """Round a Decimal half up to `places` decimal places."""
    factor = 10 ** places
    scaled = value * factor
    whole = int(scaled)
    if scaled - whole >= Decimal("0.5"):
        whole += 1
    return Decimal(whole) / factor


def _invoice_total(invoice):
    net = sum(Decimal(line.quantity * line.unit_pence) / 100 for line in invoice.lines)
    return round_half_up(net * (1 + Decimal(SETTINGS.vat_rate) / 100))


def invoice_total(invoice):
    """The total of an invoice, VAT included."""
    return _invoice_total(invoice)
