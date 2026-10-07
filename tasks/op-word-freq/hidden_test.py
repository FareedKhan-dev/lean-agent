import random
import re

from _hidden_kit import check, report, run_cli

TOP = [("kettle", 15), ("toaster", 13), ("mixer", 12), ("blender", 11), ("grinder", 10),
       ("juicer", 9), ("steamer", 8), ("fryer", 7), ("roaster", 6), ("scale", 5)]
REST = [("lamp", 3), ("rug", 2), ("desk", 1), ("chair", 1)]


def orders_text():
    words = []
    for word, n in TOP + REST:
        forms = [word, word.capitalize(), word.upper(), word + ",", word + ".", f"({word})", word + "!"]
        words += [forms[i % len(forms)] for i in range(n)]
    random.Random(7).shuffle(words)
    return "\n".join(" ".join(words[i:i + 9]) for i in range(0, len(words), 9)) + "\n"


def listed(stdout):
    """(word, numbers on its line) for every output line that names exactly one word."""
    rows = []
    for line in stdout.splitlines():
        words = re.findall(r"[^\W\d_]+", line)
        if len(words) == 1:
            rows.append((words[0].casefold(), [int(x) for x in re.findall(r"\d+", line)]))
    return rows


def top_ten():
    with open("orders.txt", "w", encoding="utf-8") as f:
        f.write(orders_text())
    p = run_cli(["wordfreq.py", "orders.txt"])
    assert p.returncode == 0, p.stderr[-200:]
    rows = listed(p.stdout)
    assert len(rows) == 10, f"{len(rows)} word lines"
    for (word, numbers), (want, count) in zip(rows, TOP):
        assert word == want and count in numbers, f"got {word} {numbers}, expected {want} {count}"
    return True


correct = check("the ten most common words, most common first, with their counts", top_ten)
report(correct)
