class InvoiceSettings:
    """Invoice settings, so the currency and VAT rate can be changed in one place."""

    def __init__(self, currency="GBP", vat_rate=20):
        self.currency = currency
        self.vat_rate = vat_rate


SETTINGS = InvoiceSettings()
