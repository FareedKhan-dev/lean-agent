"""The CSV export used before the 2024 rewrite."""
import csv


def export_legacy(invoices, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for invoice in invoices:
            writer.writerow([invoice.number, invoice.customer, invoice.issued])
