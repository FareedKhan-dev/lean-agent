import csv
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "GBP"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def rounded(self):
        return Money(self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), self.currency)


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    cost: Money


class ExpenseReader:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                yield Expense(row["date"], row["category"], Money(Decimal(row["amount"])))


class Ledger:
    def __init__(self):
        self.by_category = {}

    def post(self, expense):
        current = self.by_category.get(expense.category, Money(Decimal("0")))
        self.by_category[expense.category] = current + expense.cost

    def totals(self):
        return {c: m.rounded().amount for c, m in self.by_category.items()}


def totals_by_category(path):
    """Total spent per category in the expenses CSV at `path` (columns: date, category, amount)."""
    ledger = Ledger()
    for expense in ExpenseReader(path):
        ledger.post(expense)
    return ledger.totals()
