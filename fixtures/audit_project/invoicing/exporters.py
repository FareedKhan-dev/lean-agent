import json
import sys


def export(invoice, fmt):
    """Export an invoice in the named format: json or csv."""
    return getattr(sys.modules[__name__], f"to_{fmt}")(invoice)


def to_json(invoice):
    return json.dumps({"number": invoice.number, "customer": invoice.customer})


def to_csv(invoice):
    return f"{invoice.number},{invoice.customer}"
