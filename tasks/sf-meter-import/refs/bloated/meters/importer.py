import csv
import logging
from dataclasses import dataclass, field

log = logging.getLogger(__name__)


@dataclass
class ImportReport:
    total: float = 0.0
    accepted: int = 0
    rejected: list = field(default_factory=list)


class RowValidator:
    required = ("meter_id", "kwh")

    def validate(self, row):
        for column in self.required:
            if row.get(column) in (None, ""):
                raise ValueError(f"missing {column}")
        value = float(row["kwh"])
        if value != value:
            raise ValueError("kwh is NaN")
        return value


class MeterImporter:
    def __init__(self, validator=None):
        self.validator = validator or RowValidator()

    def run(self, path):
        report = ImportReport()
        with open(path, newline="", encoding="utf-8") as f:
            for line_no, row in enumerate(csv.DictReader(f), start=2):
                try:
                    report.total += self.validator.validate(row)
                    report.accepted += 1
                except (ValueError, TypeError) as exc:
                    report.rejected.append((line_no, str(exc)))
                    log.warning("line %d skipped: %s", line_no, exc)
        return report


def total_kwh(path):
    """Total kWh in the meter export CSV at `path` (columns: meter_id, kwh)."""
    return MeterImporter().run(path).total
