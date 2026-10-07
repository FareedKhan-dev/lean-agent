from _hidden_kit import check, report, run_cli


def products(p):
    return [ln.split()[0] for ln in p.stdout.splitlines() if ln and not ln.startswith(("units sold", "-"))]


def usage_error(p):
    return p.returncode != 0 and "Traceback" not in p.stderr and "usage" in p.stderr.lower()


plain = run_cli(["report.py"])
since = run_cli(["report.py", "--since", "2026-03-03"])
both = run_cli(["report.py", "--since", "2026-03-02", "--limit", "2"])
bad_date = run_cli(["report.py", "--since", "2026-13-01"])
bad_limit = run_cli(["report.py", "--limit", "many"])

correct = (check("no options: every product, best first",
                 lambda: plain.returncode == 0 and products(plain) == ["kettle", "mixer", "toaster", "blender"])
           and check("--since counts only sales on or after the day",
                     lambda: since.returncode == 0 and products(since) == ["toaster", "blender", "mixer", "kettle"])
           and check("--since and --limit together",
                     lambda: both.returncode == 0 and products(both) == ["mixer", "toaster"]))
quality = (check("a bad date gives a usage error, not a traceback", lambda: usage_error(bad_date))
           and check("a non-numeric limit gives a usage error, not a traceback", lambda: usage_error(bad_limit)))
report(correct, quality=quality)
