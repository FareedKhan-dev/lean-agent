def on_issue(invoice):
    """Called for every issued invoice; app.py loads this module by name."""
    return f"issued {invoice.number}"
