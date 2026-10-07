from dataclasses import dataclass, field


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
