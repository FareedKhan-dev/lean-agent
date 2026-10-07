"""Assemble lean_agent_course.ipynb from the part sources in _build/cells/.

A part source is plain text split into cells by marker lines:

    #%% md
    some markdown
    #%% code
    some python

Placeholders are resolved at build time, so every number quoted in prose comes
from an experiment file and cannot drift away from what the code printed:

    {{SYSTEM_NAME}} {{CMD}}                     names (one constant each)
    {{exp:main.h1.ratio:.2f}}                   value from artifacts/exp_main.json
    {{pick:main.h1.verdict|SUPPORTED=text|REJECTED=text}}
                                                text chosen by a recorded verdict

A missing value renders as [pending: ...] so a smoke build still works; lint
refuses to pass a notebook that still contains one.
"""
import base64
import json
import re
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CELLS_DIR = HERE / "cells"
ART = ROOT / "artifacts"
OUT = ROOT / "lean_agent_course.ipynb"

SYSTEM_NAME = "lean-agent"
CMD = "lean"

MARKER = re.compile(r"^#%% (md|code)\s*$")
PLACEHOLDER = re.compile(r"\{\{(.+?)\}\}")


def split_cells(text):
    cells, kind, buf = [], None, []
    for line in text.splitlines():
        m = MARKER.match(line)
        if m:
            if kind:
                cells.append((kind, "\n".join(buf).strip("\n")))
            kind, buf = m.group(1), []
        else:
            buf.append(line)
    if kind:
        cells.append((kind, "\n".join(buf).strip("\n")))
    return [c for c in cells if c[1].strip()]


def lookup(path):
    """'main.h1.ratio' -> artifacts/exp_main.json['h1']['ratio'], or None."""
    name, *keys = path.split(".")
    f = ART / f"exp_{name}.json"
    if not f.exists():
        return None
    value = json.loads(f.read_text(encoding="utf-8"))
    for k in keys:
        if isinstance(value, list) and k.isdigit():
            k = int(k)
        try:
            value = value[k]
        except (KeyError, IndexError, TypeError):
            return None
    return value


def resolve(match):
    body = match.group(1).strip()
    if body == "SYSTEM_NAME":
        return SYSTEM_NAME
    if body == "CMD":
        return CMD
    if body.startswith("exp:"):
        ref, _, fmt = body[4:].partition(":")
        value = lookup(ref)
        if value is None:
            return f"[pending: {ref}]"
        try:
            return format(value, fmt) if fmt else str(value)
        except (TypeError, ValueError):
            return str(value)
    if body.startswith("pick:"):
        ref, *options = body[5:].split("|")
        value = lookup(ref.strip())
        choices = dict(o.split("=", 1) for o in options if "=" in o)
        if value is None or str(value) not in choices:
            return f"[pending: {ref.strip()}]"
        return choices[str(value)]
    return match.group(0)  # not ours, leave it alone


DIAGRAMS = ART / "diagrams"
DIAGRAM = re.compile(r"\{\{diagram:([\w-]+)\}\}")


def embed_diagrams(cell):
    """Replace {{diagram:name}} with the rendered image, attached to the cell itself, so the
    notebook shows its diagrams in VS Code, Jupyter or a web viewer without any extension."""
    names = DIAGRAM.findall(cell.source)
    if not names:
        return cell
    attachments = {}
    for name in names:
        png = DIAGRAMS / f"{name}.png"
        if png.exists():
            attachments[f"{name}.png"] = {"image/png": base64.b64encode(png.read_bytes()).decode("ascii")}
            cell.source = cell.source.replace("{{diagram:%s}}" % name, f"![{name}](attachment:{name}.png)")
        else:
            cell.source = cell.source.replace("{{diagram:%s}}" % name, f"[pending: diagram {name}]")
    if attachments:
        cell["attachments"] = attachments
    return cell


def build(out=OUT, upto=None):
    parts = sorted(CELLS_DIR.glob("part*.cells"))
    nb = new_notebook()
    nb.metadata = {
        "kernelspec": {"name": "python3", "display_name": "Python 3 (ipykernel)", "language": "python"},
        "language_info": {"name": "python"},
    }
    for part in parts:
        # compare the "partNN" prefix only: "part01_measure" > "part01" as whole strings,
        # which once excluded the very part that was asked for and still reported OK
        if upto and part.stem.split("_")[0] > upto:
            break
        for i, (kind, src) in enumerate(split_cells(part.read_text(encoding="utf-8"))):
            if kind == "md":
                src = PLACEHOLDER.sub(resolve, src)
                cell = embed_diagrams(new_markdown_cell(src))
            else:
                src = src.replace("{{SYSTEM_NAME}}", SYSTEM_NAME).replace("{{CMD}}", CMD)
                cell = new_code_cell(src)
            cell["id"] = f"{part.stem.split('_')[0]}-{i:03d}"
            nb.cells.append(cell)
    nbformat.write(nb, str(out))
    return nb


if __name__ == "__main__":
    upto = sys.argv[1] if len(sys.argv) > 1 else None
    nb = build(upto=upto)
    md = sum(c.cell_type == "markdown" for c in nb.cells)
    print(f"built {OUT.name}: {len(nb.cells)} cells ({md} markdown, {len(nb.cells) - md} code)")
