from invoicing.models import BaseInvoiceStore


class MemoryInvoiceStore(BaseInvoiceStore):
    def __init__(self):
        self._by_number = {}

    def save(self, invoice):
        self._by_number[invoice.number] = invoice

    def get(self, number):
        return self._by_number.get(number)


class StoreFactory:
    """Creates the configured invoice store."""

    @staticmethod
    def create(kind="memory"):
        if kind == "memory":
            return MemoryInvoiceStore()
        raise ValueError(f"unknown store {kind}")
