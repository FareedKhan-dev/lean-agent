"""Print a table of contents for a Markdown file:  python toc.py README.md"""
import argparse
import re
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Heading:
    level: int
    text: str


class Slugger(ABC):
    @abstractmethod
    def slug(self, text):
        ...


class GitHubSlugger(Slugger):
    def __init__(self):
        self.seen = Counter()

    def slug(self, text):
        base = re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")
        self.seen[base] += 1
        return base if self.seen[base] == 1 else f"{base}-{self.seen[base] - 1}"


class MarkdownScanner:
    heading = re.compile(r"(#{1,6})\s+(.+?)\s*#*\s*$")
    fence = re.compile(r"\s*(```|~~~)")

    def headings(self, lines):
        in_code = False
        for line in lines:
            if self.fence.match(line):
                in_code = not in_code
            elif not in_code and (m := self.heading.match(line)):
                yield Heading(len(m[1]), m[2])


class TocRenderer:
    def __init__(self, slugger, min_level=2, max_level=6, bullet="-", indent=2):
        self.slugger, self.min_level, self.max_level = slugger, min_level, max_level
        self.bullet, self.indent = bullet, indent

    def render(self, headings):
        out = []
        for h in headings:
            if self.min_level <= h.level <= self.max_level:
                pad = " " * self.indent * (h.level - self.min_level)
                out.append(f"{pad}{self.bullet} [{h.text}](#{self.slugger.slug(h.text)})")
        return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print a table of contents for a Markdown file.")
    parser.add_argument("path")
    parser.add_argument("--min-level", type=int, default=2)
    parser.add_argument("--max-level", type=int, default=6)
    parser.add_argument("--bullet", default="-", choices=["-", "*", "+"])
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        headings = list(MarkdownScanner().headings(f))
    print(TocRenderer(GitHubSlugger(), args.min_level, args.max_level, args.bullet, args.indent).render(headings))


if __name__ == "__main__":
    main()
