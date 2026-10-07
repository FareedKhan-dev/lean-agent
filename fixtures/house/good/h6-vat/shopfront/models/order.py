from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_pence: int


@dataclass
class Order:
    id: int
    customer_id: int
    placed: str                      # ISO date
    lines: list = field(default_factory=list)

    def total_pence(self):
        return sum(line.quantity * line.unit_pence for line in self.lines)

    def total_with_vat(self):
        return int((Decimal(self.total_pence()) * Decimal("1.2")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
