from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Line:
    description: str
    quantity: int
    unit_pence: int


@dataclass
class Invoice:
    number: str
    customer: str
    issued: str
    lines: list = field(default_factory=list)


class BaseInvoiceStore(ABC):
    """Where invoices are kept."""

    @abstractmethod
    def save(self, invoice):
        ...

    @abstractmethod
    def get(self, number):
        ...
