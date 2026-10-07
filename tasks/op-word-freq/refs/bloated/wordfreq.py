"""Print the most common words in a text file:  python wordfreq.py FILE"""
import argparse
import csv
import json
import re
import sys
from abc import ABC, abstractmethod
from collections import Counter


class Tokenizer(ABC):
    @abstractmethod
    def tokens(self, text):
        ...


class RegexTokenizer(Tokenizer):
    def __init__(self, pattern=r"[^\W\d_]+", fold_case=True, min_length=1):
        self.pattern = re.compile(pattern)
        self.fold_case = fold_case
        self.min_length = min_length

    def tokens(self, text):
        if self.fold_case:
            text = text.casefold()
        return [t for t in self.pattern.findall(text) if len(t) >= self.min_length]


class Reporter(ABC):
    @abstractmethod
    def write(self, rows, out):
        ...


class PlainReporter(Reporter):
    def write(self, rows, out):
        for word, count in rows:
            out.write(f"{word} {count}\n")


class JsonReporter(Reporter):
    def write(self, rows, out):
        json.dump([{"word": w, "count": c} for w, c in rows], out, indent=2)


class CsvReporter(Reporter):
    def write(self, rows, out):
        writer = csv.writer(out)
        writer.writerow(["word", "count"])
        writer.writerows(rows)


REPORTERS = {"plain": PlainReporter, "json": JsonReporter, "csv": CsvReporter}


class WordFrequency:
    def __init__(self, tokenizer=None, stopwords=frozenset()):
        self.tokenizer = tokenizer or RegexTokenizer()
        self.stopwords = stopwords
        self.counts = Counter()

    def feed(self, text):
        self.counts.update(t for t in self.tokenizer.tokens(text) if t not in self.stopwords)

    def top(self, n):
        return self.counts.most_common(n)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Most common words in a text file.")
    parser.add_argument("file")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-length", type=int, default=1)
    parser.add_argument("--format", choices=sorted(REPORTERS), default="plain")
    parser.add_argument("--stopwords", help="a file with one stop word per line")
    parser.add_argument("--encoding", default="utf-8")
    args = parser.parse_args(argv)
    stopwords = frozenset()
    if args.stopwords:
        with open(args.stopwords, encoding=args.encoding) as f:
            stopwords = frozenset(line.strip().casefold() for line in f if line.strip())
    counter = WordFrequency(RegexTokenizer(min_length=args.min_length), stopwords)
    with open(args.file, encoding=args.encoding) as f:
        for line in f:
            counter.feed(line)
    REPORTERS[args.format]().write(counter.top(args.top), sys.stdout)


if __name__ == "__main__":
    main()
