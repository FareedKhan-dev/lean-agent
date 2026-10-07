from invoicing import flags
from invoicing.totals import invoice_total


def render_text(invoice):
    if flags.PDF_V2:
        return _render_v2(invoice)
    lines = [f"Invoice {invoice.number} for {invoice.customer}"]
    lines += [f"  {line.quantity} x {line.description}" for line in invoice.lines]
    lines.append(f"Total: {invoice_total(invoice)}")
    return "\n".join(lines)


def _render_v2(invoice):
    raise NotImplementedError("the new layout was never finished")
