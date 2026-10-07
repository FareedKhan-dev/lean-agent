from itertools import islice

from _hidden_kit import check, find, load, raises, report, within

batches = find(load("sync.chunks"), "batches")
db, upload = load("sync.db"), load("sync.upload")


def lists(result, cap=10_000):
    """The batches as lists, never more than `cap` of them, so a runaway generator cannot hang the test."""
    return [list(b) for b in islice(result, cap)]


def uploaded(rows, size):
    upload.SENT.clear()
    upload.upload_all(db.connect([(f"SKU{i:04d}", i) for i in range(rows)]), size=size)
    return [len(b) for b in upload.SENT]


correct = batches is not None and all([
    check("7 items in threes: 3, 3 and 1", lambda: lists(batches(list(range(7)), 3)) == [[0, 1, 2], [3, 4, 5], [6]]),
    check("an exact fit has no empty batch at the end",
          lambda: lists(batches(list(range(6)), 3)) == [[0, 1, 2], [3, 4, 5]]),
    check("no items, no batches", lambda: lists(batches([], 3)) == []),
    check("a generator works as well as a list",
          lambda: lists(batches((i for i in range(5)), 2)) == [[0, 1], [2, 3], [4]]),
    check("upload_all sends every record from the cursor", lambda: uploaded(1203, 500) == [500, 500, 203]),
    check("a size below 1 raises ValueError",
          lambda: within(2, lambda: raises(lambda: lists(batches([1, 2], 0), cap=10), ValueError)))])
report(correct)
