"""Print a table of contents for a Markdown file:  python toc.py README.md"""
import re
import sys


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        for line in f:
            m = re.match(r"(#{2,6})\s+(.*)", line)
            if m:
                text = m.group(2).strip()
                print("  " * (len(m.group(1)) - 2) + f"- [{text}](#{text.lower().replace(' ', '-')})")


if __name__ == "__main__":
    main()
