"""Dump what an executed notebook printed, cell by cell, so prose can be written
against real numbers.  python _build/inspect_outputs.py out/smoke.ipynb [--from ID] [--to ID]
"""
import argparse
import re
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent


LEAK_MARKERS = {str(Path.home()).lower(), Path.home().as_posix().lower()}


def leaks(text):
    """True if an absolute path to anything under the user's home folder was printed."""
    low = text.lower().replace("\\\\", "\\")
    return any(m in low for m in LEAK_MARKERS)


def scrub(text):
    for p in {str(ROOT), str(ROOT).replace("\\", "/"), str(ROOT.parent), str(ROOT.parent).replace("\\", "/")}:
        text = text.replace(p, "<root>")
    return re.sub(r"ms-[0-9a-f-]{20,}", "ms-****", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notebook")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--width", type=int, default=4000)
    args = ap.parse_args()
    path = Path(args.notebook)
    if not path.is_absolute():
        path = (Path(__file__).parent / path) if (Path(__file__).parent / path).exists() else ROOT / path
    nb = nbformat.read(str(path), as_version=4)
    live = args.start is None
    for cell in nb.cells:
        cid = cell.get("id", "?")
        if args.start and cid == args.start:
            live = True
        if not live:
            continue
        if cell.cell_type == "markdown":
            first = cell.source.strip().splitlines()[0] if cell.source.strip() else ""
            if first.startswith("#"):
                print(f"\n######## {cid}  {first[:110]}")
        else:
            print(f"\n---- {cid}  {cell.source.strip().splitlines()[0][:100] if cell.source.strip() else ''}")
            for o in cell.get("outputs", []):
                if o.output_type == "stream":
                    if leaks(o.text):
                        print("!!! ABSOLUTE PATH PRINTED IN THIS OUTPUT")
                    print(scrub(o.text)[: args.width])
                elif o.output_type == "error":
                    print(f"!!! {o.ename}: {scrub(o.evalue)[:600]}")
                elif o.output_type in ("display_data", "execute_result"):
                    data = o.get("data", {})
                    if "image/png" in data:
                        print("[image/png]")
                    elif "application/vnd.jupyter.widget-view+json" in data:
                        print("[widget]")
                    elif "text/html" in data:
                        print("[html] " + scrub(re.sub(r"<[^>]+>", " ", data["text/html"]))[:300])
                    elif "text/plain" in data:
                        print("[out] " + scrub(data["text/plain"])[:600])
        if args.end and cid == args.end:
            break


if __name__ == "__main__":
    main()
