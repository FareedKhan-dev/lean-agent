"""Print units sold per product, best sellers first."""
import sys
from collections import Counter

from formatting import rule, units
from sales_data import SALES


def totals(rows):
    counts = Counter()
    for day, product, n in rows:
        counts[product] += n
    return counts.most_common()


def main(argv=None):
    print("units sold by product")
    print(rule())
    for product, n in totals(SALES):
        print(f"{product:<10} {units(n)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
