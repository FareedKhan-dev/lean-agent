"""Print units sold per product, best sellers first."""
import argparse
import sys
from collections import Counter
from datetime import date

from formatting import rule, units
from sales_data import SALES


def totals(rows):
    counts = Counter()
    for day, product, n in rows:
        counts[product] += n
    return counts.most_common()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Units sold per product.")
    parser.add_argument("--since", type=date.fromisoformat, help="only count sales on or after YYYY-MM-DD")
    parser.add_argument("--limit", type=int, help="show only the top N products")
    args = parser.parse_args(argv)
    rows = [r for r in SALES if args.since is None or date.fromisoformat(r[0]) >= args.since]
    print("units sold by product")
    print(rule())
    for product, n in totals(rows)[:args.limit]:
        print(f"{product:<10} {units(n)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
