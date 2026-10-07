"""Check a built notebook, and everything shipped beside it, before anyone else reads it.

    python _build/lint.py lean_agent_course.ipynb --ban NAME --ban NAME ...

Names that must never appear are passed on the command line, so this file does not contain
them either. Exits 1 if any check fails; prints counts either way.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

CHARACTERS = {"—": "em dash", "–": "en dash", "→": "arrow", "←": "arrow", "⇒": "arrow",
              "�": "replacement character", "â€": "mojibake", "Ã©": "mojibake"}
PHRASES = ["delve", "dive in", "dive into", "seamless", "leverage", "unlock", "in today's", "it's worth noting",
           "it is worth noting", "inspired by", "game-changer", "game changer", "in conclusion", "furthermore,",
           "moreover,", "robust and scalable", "cutting-edge", "a testament to", "navigate the", "embark"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅❌]")
ABSOLUTE = re.compile(r"(?i)\b[a-z]:[\\/]+users[\\/]|/users/[a-z]|/home/[a-z]|appdata[\\/]")   # a leak, not a test input
LONG_FLOAT = re.compile(r"(?<![\w.])\d+\.\d{6,}(?![\w.])")
FIG_OUT = re.compile(r"\[fig (\d+)\] (\w+)\.png")
FIG_READ = re.compile(r"Reading FIG (\d+) \((\w+)\)")


def joined(value):
    return value if isinstance(value, str) else "".join(value)


def text_of(cell):
    """A cell's source, and for code cells the text of every output."""
    out = [joined(cell["source"])]
    for o in cell.get("outputs", []):
        if "text" in o:
            out.append(joined(o["text"]))
        for kind in ("text/plain", "text/html", "text/markdown"):
            data = o.get("data", {}).get(kind)
            if data:
                out.append(joined(data))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notebook")
    ap.add_argument("--ban", action="append", default=[], help="a name that must appear nowhere")
    args = ap.parse_args()
    nb = json.loads(Path(args.notebook).read_text(encoding="utf-8"))
    cells, problems = nb["cells"], []

    def problem(where, what):
        problems.append(f"{where}: {what}")

    key_file = ROOT.parent / "modelscope.txt"
    key = key_file.read_text(encoding="utf-8").strip() if key_file.exists() else ""
    shipped = [Path(args.notebook)] + sorted((ROOT / "artifacts").glob("*.json")) + sorted((ROOT / "skills").rglob("*.md"))
    for path in shipped:
        raw = path.read_bytes()
        if key and key.encode() in raw:
            problem(path.name, "CONTAINS THE API KEY")
        low = raw.decode("utf-8", "replace").lower()
        for name in args.ban:
            if name.lower() in low:
                problem(path.name, f"mentions a banned name ({len(name)} letters)")

    paragraphs = Counter()
    code_cells = figures = readings = diagrams = widgets = 0
    fig_outputs, fig_readings = {}, {}
    for cell in cells:
        cid, src, full = cell.get("id", "?"), joined(cell["source"]), text_of(cell)
        for ch, what in CHARACTERS.items():
            if ch in full:
                problem(cid, f"{what} ({full.count(ch)}x)")
        if EMOJI.search(full):
            problem(cid, "emoji")
        lower = full.lower()
        for phrase in PHRASES:
            if re.search(rf"(?<![\w-]){re.escape(phrase)}(?![\w-])", lower) and cell["cell_type"] == "markdown":
                problem(cid, f"phrase '{phrase}'")
        if ABSOLUTE.search(full):
            problem(cid, f"absolute path: {ABSOLUTE.search(full).group(0)}")
        if "[pending:" in full:
            problem(cid, "unresolved number: " + re.search(r"\[pending: [^\]]*\]", full).group(0))
        if cell["cell_type"] == "markdown":
            if "{{" in src:
                problem(cid, "unresolved placeholder")
            for m in LONG_FLOAT.finditer(src):
                problem(cid, f"unrounded number {m.group(0)}")
            if "```mermaid" in src:
                problem(cid, "a mermaid block: most viewers show it as text; render it with render_diagrams.py")
            for name in re.findall(r"!\[[^\]]*\]\(attachment:([^)]+)\)", src):
                diagrams += 1
                if name not in cell.get("attachments", {}):
                    problem(cid, f"diagram {name} is referenced but not attached")
            for m in FIG_READ.finditer(src):
                fig_readings[int(m.group(1))] = m.group(2)
            for para in re.split(r"\n\s*\n", src):
                if len(para) > 120:
                    paragraphs[para.strip()] += 1
        else:
            code_cells += 1
            if not cell.get("outputs"):
                problem(cid, "code cell without output")
            for o in cell.get("outputs", []):
                if o.get("output_type") == "error":
                    problem(cid, f"error output: {o.get('ename')}")
                if o.get("output_type") == "execute_result":
                    problem(cid, "a stray Out[] value; end the cell with a print or a call that returns None")
            for m in FIG_OUT.finditer(full):
                fig_outputs[int(m.group(1))] = m.group(2)
            for m in LONG_FLOAT.finditer("\n".join(joined(o.get("text", "")) for o in cell.get("outputs", []))):
                problem(cid, f"unrounded number printed: {m.group(0)}")
            if re.search(r"^W = widgets\(\)", src, re.M):
                widgets += 1
                if not re.search(r"^else:\n    print\(", src, re.M):
                    problem(cid, "a widget without a static fallback")
    for para, n in paragraphs.items():
        if n > 1:
            problem("markdown", f"a paragraph repeated {n}x: {para[:70]}...")
    for n, name in sorted(fig_outputs.items()):
        if fig_readings.get(n) != name:
            problem(f"FIG {n}", f"{name} has no matching 'Reading FIG {n} ({name})' paragraph")
    for n, name in sorted(fig_readings.items()):
        if fig_outputs.get(n) != name:
            problem(f"FIG {n}", f"a Reading for {name} that no figure produced")
    figures, readings = len(fig_outputs), len(fig_readings)
    kernel = nb.get("metadata", {}).get("kernelspec", {})
    if kernel.get("name") != "python3":
        problem("metadata", f"kernelspec is {kernel.get('name')!r}, not the neutral python3")

    print(f"[lint] {len(cells)} cells ({code_cells} code), {figures} figures with {readings} readings, "
          f"{diagrams} diagrams, {widgets} widget cells")
    for p in problems:
        print("  " + p)
    print(f"[lint] {'PASSED' if not problems else f'FAILED with {len(problems)} problems'}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
