"""Print units sold per product, best sellers first."""
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
    argv = sys.argv[1:] if argv is None else argv
    since = limit = None
    if "--since" in argv:
        since = date.fromisoformat(argv[argv.index("--since") + 1])
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    rows = [r for r in SALES if since is None or date.fromisoformat(r[0]) >= since]
    print("units sold by product")
    print(rule())
    for product, n in totals(rows)[:limit]:
        print(f"{product:<10} {units(n)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
