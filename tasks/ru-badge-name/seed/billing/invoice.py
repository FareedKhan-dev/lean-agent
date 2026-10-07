from people.names import display_name


def invoice_header(first, last, number):
    return f"Invoice {number} for {display_name(first, last)}"
