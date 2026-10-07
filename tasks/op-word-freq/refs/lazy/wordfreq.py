"""Print the ten most common words in a text file:  python wordfreq.py FILE"""
import sys
from collections import Counter


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        for word, count in Counter(f.read().split()).most_common(10):
            print(f"{word} {count}")


if __name__ == "__main__":
    main()
