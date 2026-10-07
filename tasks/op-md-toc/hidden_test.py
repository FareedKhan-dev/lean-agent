import re

from _hidden_kit import check, report, run_cli

CLUB = """# Kettle Club

A club for people who take tea seriously.

## Getting started

### Install

```bash
# one line is enough
pip install kettleclub
```

### Example

```python
from kettleclub import brew
```

## Recipes

### Example

## What's new?

Release notes follow this pattern:

```markdown
## [2.0.0] - 2026-04-01
### Changed
- Brewing times are now in seconds
```

## API
"""
ITEM = re.compile(r"^(\s*)[-*+]\s+\[(.+?)\]\(#([^)\s]+)\)\s*$")


def entries():
    with open("CLUB.md", "w", encoding="utf-8") as f:
        f.write(CLUB)
    p = run_cli(["toc.py", "CLUB.md"])
    assert p.returncode == 0, p.stderr[-200:]
    rows = [(len(m[1].expandtabs(4)), m[2], m[3]) for m in map(ITEM.match, p.stdout.splitlines()) if m]
    assert rows, "no linked bullet lines in the output"
    return rows


def structure():
    rows = entries()
    texts = [t for _, t, _ in rows]
    plain = {t: (indent, a) for indent, t, a in rows if t in ("Getting started", "Install", "Recipes", "API")}
    assert "Kettle Club" not in texts, "the title is listed"
    assert [t for t in texts if t in plain] == ["Getting started", "Install", "Recipes", "API"], texts
    assert plain["Getting started"][1] == "getting-started" and plain["API"][1] == "api", plain
    assert plain["Install"][0] > plain["Getting started"][0] == plain["Recipes"][0], plain
    assert plain["Getting started"][0] == 0, "top-level bullets are indented, so GitHub shows them as code"
    return True


def github_details():
    rows = entries()
    texts = [t for _, t, _ in rows]
    assert not any(t.startswith("[2.0.0]") or t == "Changed" for t in texts), "lines inside a code block were listed"
    anchors = {t: [a for _, t2, a in rows if t2 == t] for t in ("Example", "What's new?")}
    assert anchors["What's new?"] == ["whats-new"], anchors
    assert anchors["Example"] == ["example", "example-1"], anchors
    return True


correct = check("headings become linked bullets, nested by level, without the title", structure)
quality = check("code blocks, punctuation and repeated headings are handled the way GitHub does", github_details)
report(correct, quality=quality)
