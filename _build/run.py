"""Execute the course notebook headlessly.

    python _build/run.py smoke  [--upto part03]   scripted model, zero API calls
    python _build/run.py collect [--upto part07]  live calls, every reply cached
    python _build/run.py replay                   cache only; a miss is an error

Every directory Jupyter, IPython, matplotlib and tempfile would normally create
in the user profile is pointed inside lean_agent/.runtime, so nothing lands
outside the project.
"""
import argparse
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUNTIME = ROOT / ".runtime"
OUT_DIR = HERE / "out"

REDIRECTS = {
    "JUPYTER_RUNTIME_DIR": RUNTIME / "jupyter_runtime",
    "JUPYTER_DATA_DIR": RUNTIME / "jupyter_data",
    "JUPYTER_CONFIG_DIR": RUNTIME / "jupyter_config",
    "IPYTHONDIR": RUNTIME / "ipython",
    "MPLCONFIGDIR": RUNTIME / "matplotlib",
    "TEMP": RUNTIME / "tmp",
    "TMP": RUNTIME / "tmp",
    "TMPDIR": RUNTIME / "tmp",
}


def unpack_ledger():
    """The ledger of live answers ships gzipped (GitHub refuses files over 100 MB); unpack it once."""
    import gzip
    import shutil
    db = ROOT / "artifacts" / "cache" / "llm.sqlite"
    packed = db.with_name("llm.sqlite.gz")
    if not db.exists() and packed.exists():
        print(f"[ledger] unpacking {packed.name} (about 150 MB, once)")
        with gzip.open(packed, "rb") as src, open(db, "wb") as dst:
            shutil.copyfileobj(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["smoke", "collect", "replay"])
    ap.add_argument("--upto", help="last part to include, e.g. part03")
    ap.add_argument("--timeout", type=int, default=None, help="per-cell timeout in seconds")
    args = ap.parse_args()

    if sys.platform == "win32":   # zmq needs a selector loop; the default proactor loop warns
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for key, path in REDIRECTS.items():
        path.mkdir(parents=True, exist_ok=True)
        os.environ[key] = str(path)
    os.environ["LEAN_MODE"] = args.mode
    os.environ["LEAN_HEADLESS"] = "1"        # nobody can click a widget here; the cells print their static views
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

    unpack_ledger()
    sys.path.insert(0, str(HERE))
    from build import build  # noqa: E402  (after the env is set)
    import nbformat
    from nbclient import NotebookClient

    OUT_DIR.mkdir(exist_ok=True)
    built = OUT_DIR / f"{args.mode}_input.ipynb"
    nb = build(out=built, upto=args.upto)
    target = ROOT / "lean_agent_course.ipynb" if args.mode == "replay" and not args.upto else OUT_DIR / f"{args.mode}.ipynb"

    started = time.time()
    code_total = sum(c.cell_type == "code" for c in nb.cells)
    done = {"n": 0}

    def on_executed(cell, cell_index, execute_reply):
        done["n"] += 1
        took = time.time() - started
        head = cell.source.strip().splitlines()[0][:70] if cell.source.strip() else ""
        print(f"[{done['n']:>3}/{code_total}] {cell.get('id', cell_index)}  {took:7.1f}s  {head}", flush=True)

    client = NotebookClient(
        nb,
        kernel_name="python3",
        timeout=args.timeout,
        allow_errors=False,
        store_widget_state=True,
        resources={"metadata": {"path": str(ROOT)}},
        on_cell_executed=on_executed,
    )
    try:
        client.execute()
        status = "OK"
    except Exception as e:  # keep whatever ran, so the failure can be inspected
        status = f"FAILED: {type(e).__name__}: {str(e)[:2000]}"
    nbformat.write(nb, str(target))
    ran = sum(1 for c in nb.cells if c.cell_type == "code" and c.get("execution_count"))
    print(f"\n{status}: {ran}/{code_total} code cells executed")
    print(f"wrote {target.relative_to(ROOT)} in {time.time() - started:.0f}s")
    if status == "OK" and ran < code_total:
        status = "INCOMPLETE"
    sys.exit(0 if status == "OK" else 1)


if __name__ == "__main__":
    main()
