import csv
from decimal import Decimal

from expenses import totals_by_category


def statement_totals(path):
    """Category totals from the bank's monthly statement export."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["category"]: Decimal(row["total"]) for row in csv.DictReader(f)}


def mismatches(expenses_csv, statement_csv):
    """Categories where our books and the bank statement disagree."""
    ours, bank = totals_by_category(expenses_csv), statement_totals(statement_csv)
    return sorted(c for c in ours.keys() | bank.keys() if ours.get(c) != bank.get(c))
