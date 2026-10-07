def is_balanced(invoice):
    """True if every line has a positive quantity. Used by the test suite."""
    return all(line.quantity > 0 for line in invoice.lines)
