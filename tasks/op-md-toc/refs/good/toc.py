"""Print a table of contents for a Markdown file:  python toc.py README.md"""
import re
import sys
from collections import Counter

HEADING = re.compile(r"(#{2,6})\s+(.+?)\s*#*\s*$")


def anchor(text, seen):
    """GitHub's anchor: lowercase, punctuation dropped, spaces to hyphens, repeats numbered."""
    slug = re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")
    seen[slug] += 1
    return slug if seen[slug] == 1 else f"{slug}-{seen[slug] - 1}"


def toc(lines):
    seen, in_code, out = Counter(), False, []
    for line in lines:
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
        elif not in_code and (m := HEADING.match(line)):
            out.append("  " * (len(m[1]) - 2) + f"- [{m[2]}](#{anchor(m[2], seen)})")
    return out


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        print("\n".join(toc(f)))
