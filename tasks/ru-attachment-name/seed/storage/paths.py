"""Turning names that come from outside into names that are safe on every disk we use."""
import re
import unicodedata

RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def safe_filename(name, max_length=80):
    """'../../Report final.PDF' -> 'Report_final.PDF'; 'CON.txt' -> '_CON.txt'.
    NFKC-normalises, drops any directory part, replaces unsafe characters with '_'."""
    name = unicodedata.normalize("NFKC", name)
    name = name.replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^\w.\-]+", "_", name).strip("._") or "file"
    stem = name.partition(".")[0]
    if stem.upper() in RESERVED:
        name = "_" + name
    return name[:max_length]
