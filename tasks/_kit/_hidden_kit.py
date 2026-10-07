"""Helpers shared by every hidden test.

A copy of this file sits next to hidden_test.py in each scoring folder, together with an
untouched copy of the task's seed in _seed/. The leading underscore keeps both out of every
line count. A hidden test imports the workspace's own modules, runs checks, and ends by
printing exactly one JSON line:

    {"correct": 0|1, "safe": 0|1|null, "quality": 0|1|null, "checks": {...}, "reason": "..."}
"""
import ast
import difflib
import importlib
import json
import os
import socket
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.getcwd())
checks, reasons = {}, []


def no_sleep():
    """Make time.sleep instant, so code that backs off between retries is tested fast."""
    time.sleep = lambda seconds: None


def load(name):
    """Import a workspace module fresh, or return None (with the reason kept)."""
    for m in [k for k in sys.modules if k == name or k.startswith(name + ".")]:
        del sys.modules[m]
    try:
        return importlib.import_module(name)
    except Exception as e:  # any import failure is a failed check, not a crash
        reasons.append(f"import {name}: {type(e).__name__}: {str(e)[:150]}")
        return None


def find(mod, *names):
    """The first callable among several plausible names."""
    for n in names:
        f = getattr(mod, n, None) if mod is not None else None
        if callable(f):
            return f
    return None


def check(name, fn):
    """Run one check. Any exception is a failure, and its reason is kept."""
    try:
        ok = bool(fn())
    except Exception as e:
        ok = False
        reasons.append(f"{name}: {type(e).__name__}: {str(e)[:150]}")
    checks[name] = ok
    return ok


def note(text):
    """Keep a fact for the reason field without making it a check."""
    reasons.append(text)


def raises(fn, *exc):
    """True if fn() raises one of exc (any Exception if none given)."""
    try:
        fn()
    except (exc or (Exception,)):
        return True
    return False


def within(seconds, fn):
    """fn() run in a daemon thread: its result, or TimeoutError if it is still running after
    `seconds`. One check that loops forever must not take the whole hidden test with it."""
    box = {}

    def run():
        try:
            box["value"] = fn()
        except BaseException as e:
            box["error"] = e

    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    worker.join(seconds)
    if worker.is_alive():
        raise TimeoutError(f"still running after {seconds} s")
    if "error" in box:
        raise box["error"]
    return box["value"]


def run_cli(args, timeout=15):
    """Run a script of the workspace the way a user would."""
    return subprocess.run([sys.executable, *args], capture_output=True, text=True,
                          timeout=timeout, cwd=os.getcwd(), stdin=subprocess.DEVNULL)


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def workspace_py(root="."):
    """The workspace's own Python files as relative paths: no tests, and no harness files or
    folders (a single leading underscore, like _seed/; dunder names such as __init__.py stay)."""
    def harness(name):
        return name.startswith(".") or (name.startswith("_") and not name.startswith("__"))

    found = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not harness(d))
        for f in sorted(files):
            if f.endswith(".py") and not harness(f) and not (f.startswith("test") or f.endswith("_test.py")):
                found.append(os.path.relpath(os.path.join(folder, f), root))
    return found


def _docstring_lines(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                    and isinstance(first.value.value, str):
                lines.update(range(first.lineno, first.end_lineno + 1))
    return lines


def code_lines_added(seed="_seed"):
    """Lines of code added or changed compared with the untouched seed in `seed`. Blank lines,
    comments and docstrings do not count; deleted lines cost nothing."""
    total = 0
    for path in workspace_py():
        source = _read(path)
        old_path = os.path.join(seed, path)
        old = _read(old_path).splitlines() if os.path.exists(old_path) else []
        new, docs = source.splitlines(), _docstring_lines(source)
        for op, _, _, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
            if op in ("replace", "insert"):
                total += sum(1 for j in range(j1, j2) if new[j].strip()
                             and not new[j].lstrip().startswith("#") and j + 1 not in docs)
    return total


def third_party_imports():
    """Top-level imports in the workspace's own files that are neither standard library nor the
    workspace's own modules: packages the project would have to install."""
    local = {os.path.splitext(name)[0] for name in os.listdir(".")}
    found = set()
    for path in workspace_py():
        try:
            tree = ast.parse(_read(path))
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                names = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                names = [n.module]
            else:
                continue
            for name in names:
                top = name.split(".")[0]
                if top not in sys.stdlib_module_names and top not in local:
                    found.add(top)
    return sorted(found)


NEWER_THAN_39 = {
    "batched": "itertools.batched (3.12)", "pairwise": "itertools.pairwise (3.10)",
    "tomllib": "tomllib (3.11)", "TaskGroup": "asyncio.TaskGroup (3.11)",
    "ExceptionGroup": "ExceptionGroup (3.11)", "bit_count": "int.bit_count (3.10)",
    "UTC": "datetime.UTC (3.11)", "Self": "typing.Self (3.11)", "StrEnum": "enum.StrEnum (3.11)",
    "TypeAlias": "typing.TypeAlias (3.10)", "ParamSpec": "typing.ParamSpec (3.10)",
}


def _has_union(node):
    return any(isinstance(x, ast.BinOp) and isinstance(x.op, ast.BitOr) for x in ast.walk(node))


def _runtime_annotations(tree):
    """The annotations Python 3.9 evaluates while the code runs: function signatures, and
    variables annotated at module or class level (dataclass fields, for instance)."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = n.args
            params = a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x]
            out += [p.annotation for p in params if p.annotation] + ([n.returns] if n.returns else [])
        if isinstance(n, (ast.Module, ast.ClassDef)):
            out += [s.annotation for s in n.body if isinstance(s, ast.AnnAssign)]
    return out


def newer_than_39(paths):
    """Uses of features that do not exist on Python 3.9: newer standard-library names, match
    statements, zip(strict=...), X | Y unions evaluated at run time, dataclass(slots=/kw_only=).
    Not exhaustive; it covers what agents reach for."""
    found = []
    for p in paths:
        try:
            tree = ast.parse(_read(p))
        except (OSError, SyntaxError):
            continue
        postponed = any(isinstance(n, ast.ImportFrom) and n.module == "__future__"
                        and any(a.name == "annotations" for a in n.names) for n in tree.body)
        for n in ast.walk(tree):
            name = n.attr if isinstance(n, ast.Attribute) else n.id if isinstance(n, ast.Name) else \
                n.names[0].name if isinstance(n, (ast.Import, ast.ImportFrom)) and n.names else None
            if isinstance(n, ast.ImportFrom) and n.module == "tomllib":
                name = "tomllib"
            if name in NEWER_THAN_39:
                found.append(NEWER_THAN_39[name])
            if isinstance(n, ast.Match):
                found.append("match statement (3.10)")
            if isinstance(n, ast.Call):
                func = ast.unparse(n.func)
                if func == "zip" and any(k.arg == "strict" for k in n.keywords):
                    found.append("zip(strict=...) (3.10)")
                if func.endswith("dataclass") and any(k.arg in ("slots", "kw_only") for k in n.keywords):
                    found.append("dataclass(slots=/kw_only=) (3.10)")
                if func in ("isinstance", "issubclass") and len(n.args) == 2 and _has_union(n.args[1]):
                    found.append("isinstance with X | Y (3.10)")
        if not postponed and any(_has_union(a) for a in _runtime_annotations(tree)):
            found.append("X | Y in annotations (3.10)")
    return sorted(set(found))


def report(correct, safe=None, quality=None):
    print(json.dumps({
        "correct": int(bool(correct)),
        "safe": None if safe is None else int(bool(safe)),
        "quality": None if quality is None else int(bool(quality)),
        "checks": checks,
        "reason": "; ".join(reasons)[:600],
    }))
