"""Print units sold per product, best sellers first."""
import argparse
import sys
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from datetime import date
from typing import Callable, Optional

from formatting import rule, units
from sales_data import SALES


@dataclass(frozen=True)
class OptionSpec:
    flag: str
    type: Callable
    help: str
    default: Optional[object] = None


class Filter(ABC):
    @abstractmethod
    def apply(self, rows):
        ...


class SinceFilter(Filter):
    def __init__(self, since):
        self.since = since

    def apply(self, rows):
        if self.since is None:
            return list(rows)
        return [r for r in rows if date.fromisoformat(r[0]) >= self.since]


class ReportCommand:
    OPTIONS = (
        OptionSpec("--since", date.fromisoformat, "only count sales on or after YYYY-MM-DD"),
        OptionSpec("--limit", int, "show only the top N products"),
    )

    def __init__(self, argv=None):
        self.argv = argv
        self.parser = self._build_parser()

    def _build_parser(self):
        parser = argparse.ArgumentParser(description="Units sold per product.")
        for spec in self.OPTIONS:
            parser.add_argument(spec.flag, type=spec.type, default=spec.default, help=spec.help)
        return parser

    def run(self):
        args = self.parser.parse_args(self.argv)
        rows = SinceFilter(args.since).apply(SALES)
        self.render(totals(rows), args.limit)
        return 0

    @staticmethod
    def render(ranked, limit):
        print("units sold by product")
        print(rule())
        for product, n in ranked[:limit]:
            print(f"{product:<10} {units(n)}")


def totals(rows):
    counts = Counter()
    for day, product, n in rows:
        counts[product] += n
    return counts.most_common()


def main(argv=None):
    return ReportCommand(argv).run()


if __name__ == "__main__":
    sys.exit(main())
