"""Authoring check for task fixtures, without the sandbox (the notebook's S8 is the real
self-test, with the fence). For each task: stub must fail, lazy must fail on its axis,
good must pass, bloated must pass, and the visible test must pass for good and bloated.
task.json "expect" overrides these per reference.   python _build/check_tasks.py [task-id ...]
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "tasks"
TMP = ROOT / ".runtime" / "tmp" / "check_tasks"
ENV = {"PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
       "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""), "PATH": os.environ.get("PATH", "")}


def materialise(task_dir, dest, ref=None):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(task_dir / "seed", dest)
    if ref and (task_dir / "refs" / ref).exists():
        shutil.copytree(task_dir / "refs" / ref, dest, dirs_exist_ok=True)


def run(ws, script):
    return subprocess.run([sys.executable, script], cwd=ws, capture_output=True, text=True,
                          timeout=60, env=ENV, stdin=subprocess.DEVNULL)


def score(task_dir, ws):
    shutil.copy(task_dir / "hidden_test.py", ws / "hidden_test.py")
    shutil.copy(TASKS / "_kit" / "_hidden_kit.py", ws / "_hidden_kit.py")
    shutil.copytree(task_dir / "seed", ws / "_seed")
    try:
        p = run(ws, "hidden_test.py")
    except subprocess.TimeoutExpired:
        return {"correct": 0, "safe": 0, "quality": 0, "reason": "hidden test timed out"}
    lines = [ln for ln in p.stdout.strip().splitlines() if ln.startswith("{")]
    if not lines:
        return {"correct": 0, "safe": 0, "quality": 0, "reason": "no result: " + (p.stderr or p.stdout)[-300:]}
    return json.loads(lines[-1])


def expected(task, ref):
    exp = {"stub": {"correct": 0},
           "lazy": {"correct": 0} if task["axis"] == "correct" else {"correct": 1, task["axis"]: 0},
           "good": {"correct": 1, "safe": (1, None), "quality": (1, None)},
           "bloated": {"correct": 1, "safe": (1, None), "quality": (1, None)}}[ref]
    exp.update(task.get("expect", {}).get(ref, {}))
    return exp


def matches(result, exp):
    for k, v in exp.items():
        allowed = v if isinstance(v, (tuple, list)) else (v,)
        if result.get(k) not in allowed:
            return False
    return True


def main(ids):
    dirs = [d for d in sorted(TASKS.iterdir()) if (d / "task.json").exists()]
    if ids:
        dirs = [d for d in dirs if d.name in ids]
    bad = 0
    for d in dirs:
        task = json.loads((d / "task.json").read_text(encoding="utf-8"))
        line = []
        for ref in ("stub", "lazy", "good", "bloated"):
            ws = TMP / d.name / ref
            materialise(d, ws, None if ref == "stub" else ref)
            r = score(d, ws)
            ok = matches(r, expected(task, ref))
            if ref in ("good", "bloated"):
                materialise(d, ws, ref)
                vis = run(ws, "tests_visible.py").returncode == 0
                ok = ok and vis
                if not vis:
                    r["reason"] = "visible test fails; " + r.get("reason", "")
            bad += not ok
            line.append(f"{ref}:{'ok' if ok else 'XX'}(c{r.get('correct')} s{r.get('safe')} q{r.get('quality')})")
            if not ok:
                line.append(f"\n      reason: {r.get('reason', '')[:300]}  checks: {r.get('checks')}")
        print(f"{d.name:<24} " + "  ".join(line))
    print(f"\n{len(dirs)} tasks, {bad} unexpected results")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
