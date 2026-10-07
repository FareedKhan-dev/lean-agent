import importlib

from invoicing.dates import parse_issued
from invoicing.exporters import export
from invoicing.format import format_all
from invoicing.models import Invoice, Line
from invoicing.render import render_text
from invoicing.send import send
from invoicing.store import StoreFactory
from invoicing.templates import apply

HOOKS = ["invoicing.hooks"]


def issue(number, customer, issued, lines, outbox):
    store = StoreFactory.create()
    invoice = Invoice(number, customer, parse_issued(issued).isoformat(), [Line(*line) for line in lines])
    store.save(invoice)
    for name in HOOKS:
        importlib.import_module(name).on_issue(invoice)
    send(render_text(invoice), outbox)
    return export(invoice, "json")


if __name__ == "__main__":
    outbox = []
    print(issue("A-1", "Ann", "2026-03-02", [("kettle", 1, 2499)], outbox))
    print(format_all([2499, 120]))
    print(apply("money", 2499))
