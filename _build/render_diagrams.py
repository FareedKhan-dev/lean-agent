"""Render every diagram in _build/diagrams/*.mmd to artifacts/diagrams/<name>.png, offline.

Mermaid draws in a browser, so a headless Chrome (or Edge) opens a small local page with the
pinned mermaid build in _build/vendor/, takes a screenshot at twice the pixel density, and
Pillow crops it to the drawing. A diagram is drawn again only when its source changed. The
images are embedded in the notebook by build.py, so they show in any viewer, offline.

    python _build/render_diagrams.py            # render what changed
    python _build/render_diagrams.py --all      # render everything again
"""
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "diagrams"
OUT = ROOT / "artifacts" / "diagrams"
WORK = ROOT / ".runtime" / "diagrams"
MERMAID = HERE / "vendor" / "mermaid.min.js"
MIN_WIDTH = 2000                # pixels: a 1000px-wide notebook column then shows the design size
BROWSERS = [Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")]

# (fill, underline) pairs for mindmap branches, in the order the branches are drawn
MINDMAP = [("#b3cff2", "#2a78d6"), ("#a8e0c8", "#1baf7a"), ("#f9c99b", "#eb6834"),
           ("#f8dc85", "#eda100"), ("#cfc6ee", "#4a3aa7"), ("#f4b0af", "#e34948")]

# one palette for every diagram, the same colours as the notebook's figures
CONFIG = {
    "startOnLoad": False,
    "theme": "base",
    "fontFamily": "'Segoe UI', 'Segoe UI Emoji', Arial, sans-serif",
    "themeVariables": {
        "fontFamily": "'Segoe UI', 'Segoe UI Emoji', Arial, sans-serif", "fontSize": "17px",
        "background": "#ffffff", "primaryColor": "#eef4fc", "primaryBorderColor": "#2a78d6",
        "primaryTextColor": "#0b0b0b", "secondaryColor": "#e9f7f1", "tertiaryColor": "#fff4e5",
        "lineColor": "#6b6a65", "textColor": "#0b0b0b", "clusterBkg": "#fafaf8", "clusterBorder": "#d6d4cf",
        "edgeLabelBackground": "#ffffff", "noteBkgColor": "#fffbe6", "noteBorderColor": "#eda100",
        "noteTextColor": "#0b0b0b", "actorBkg": "#eef4fc", "actorBorder": "#2a78d6", "actorTextColor": "#0b0b0b",
        "signalColor": "#52514e", "signalTextColor": "#0b0b0b", "labelBoxBkgColor": "#fafaf8",
        "labelBoxBorderColor": "#d6d4cf", "activationBkgColor": "#e9f7f1", "activationBorderColor": "#1baf7a",
        # mindmaps colour their branches from this scale: soft tints of the figure palette, strong underlines
        **{f"cScale{i}": fill for i, (fill, _) in enumerate(MINDMAP * 2)},
        **{f"cScaleInv{i}": line for i, (_, line) in enumerate(MINDMAP * 2)},
        **{f"cScaleLabel{i}": "#0b0b0b" for i in range(12)},
        "git0": "#2a78d6", "gitBranchLabel0": "#ffffff",
    },
    "flowchart": {"curve": "basis", "htmlLabels": True, "nodeSpacing": 42, "rankSpacing": 58, "padding": 16,
                  "wrappingWidth": 460, "subGraphTitleMargin": {"top": 8, "bottom": 26}},
    "sequence": {"actorMargin": 70, "messageMargin": 42, "boxMargin": 12, "mirrorActors": False, "useMaxWidth": False},
    "mindmap": {"padding": 18},
    "state": {"padding": 12},
}

# the semantic colours a flowchart can use by writing %%STYLES%% after its first line
STYLES = """
classDef host fill:#eef4fc,stroke:#2a78d6,stroke-width:2px,color:#0b0b0b
classDef plugin fill:#e9f7f1,stroke:#1baf7a,stroke-width:2px,color:#0b0b0b
classDef lab fill:#fff4e5,stroke:#eb6834,stroke-width:2px,color:#0b0b0b
classDef warn fill:#fdecec,stroke:#e34948,stroke-width:2px,color:#0b0b0b
classDef gold fill:#fffbe6,stroke:#eda100,stroke-width:2px,color:#0b0b0b
classDef plum fill:#f3effb,stroke:#4a3aa7,stroke-width:2px,color:#0b0b0b
classDef grey fill:#f4f4f2,stroke:#8a8880,stroke-width:1.5px,color:#0b0b0b
"""

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;padding:36px;background:#ffffff}
.cluster-label div,.cluster-label span{max-width:none!important;width:auto!important;white-space:nowrap!important}</style>
<script src="%s"></script></head><body>
<pre class="mermaid">%s</pre>
<script>mermaid.initialize(%s); mermaid.run();</script>
</body></html>"""


def browser():
    for b in BROWSERS:
        if b.exists():
            return b
    sys.exit("[diagrams] no Chrome or Edge found")


def render(src_path, width=1700, height=2600):
    """Draw one diagram to a cropped PNG; return its size, or raise if nothing was drawn."""
    text = src_path.read_text(encoding="utf-8").replace("%%STYLES%%", STYLES)
    page = WORK / f"{src_path.stem}.html"
    page.write_text(PAGE % (MERMAID.as_uri(), html.escape(text), json.dumps(CONFIG)), encoding="utf-8")
    shot = WORK / f"{src_path.stem}.full.png"
    shot.unlink(missing_ok=True)
    subprocess.run([str(browser()), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--force-device-scale-factor=2", f"--window-size={width},{height}", "--virtual-time-budget=20000",
                    f"--user-data-dir={WORK / 'profile'}", f"--screenshot={shot}", page.as_uri()],
                   check=True, capture_output=True, timeout=120)
    img = Image.open(shot).convert("RGB")
    box = ImageChops.difference(img, Image.new("RGB", img.size, (255, 255, 255))).getbbox()
    if box is None:
        raise RuntimeError(f"{src_path.name}: nothing was drawn (a syntax error in the diagram?)")
    if box[2] >= img.width - 4 or box[3] >= img.height - 4:      # touching an edge: draw it on a bigger page
        return render(src_path, width + 900, height + 2000)
    margin = 28
    crop = img.crop((max(0, box[0] - margin), max(0, box[1] - margin),
                     min(img.width, box[2] + margin), min(img.height, box[3] + margin)))
    # a notebook shows an image at its pixel width, so a narrow drawing at twice the density
    # would appear twice as large as designed: centre it on a canvas of at least MIN_WIDTH
    if crop.width < MIN_WIDTH:
        canvas = Image.new("RGB", (MIN_WIDTH, crop.height), (255, 255, 255))
        canvas.paste(crop, ((MIN_WIDTH - crop.width) // 2, 0))
        crop = canvas
    # diagrams use few colours: a 256-colour palette keeps them sharp at a fraction of the size
    crop = crop.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    crop.save(OUT / f"{src_path.stem}.png", optimize=True)
    return crop.size


def main(force=False):
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    stamp = hashlib.sha256((MERMAID.read_bytes()[:4096] + json.dumps(CONFIG).encode() + STYLES.encode() + PAGE.encode()
                            + str(MIN_WIDTH).encode())).hexdigest()
    done = 0
    for src in sorted(SRC.glob("*.mmd")):
        key = hashlib.sha256(src.read_bytes() + stamp.encode()).hexdigest()
        meta = OUT / f"{src.stem}.json"
        if not force and meta.exists() and json.loads(meta.read_text())["key"] == key and (OUT / f"{src.stem}.png").exists():
            continue
        size = render(src)
        meta.write_text(json.dumps({"key": key, "size": size}))
        done += 1
        print(f"[diagrams] {src.stem:<28} {size[0]}x{size[1]}")
    print(f"[diagrams] {done} drawn, {len(list(SRC.glob('*.mmd'))) - done} unchanged")


if __name__ == "__main__":
    main(force="--all" in sys.argv)
