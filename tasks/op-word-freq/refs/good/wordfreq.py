"""Print the ten most common words in a text file:  python wordfreq.py FILE"""
import re
import sys
from collections import Counter


def top_words(text, n=10):
    """The n most common words, ignoring case; a word is a run of letters."""
    return Counter(re.findall(r"[^\W\d_]+", text.casefold())).most_common(n)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python wordfreq.py FILE")
    with open(sys.argv[1], encoding="utf-8") as f:
        for word, count in top_words(f.read()):
            print(f"{word} {count}")


if __name__ == "__main__":
    main()
