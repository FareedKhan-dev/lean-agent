import subprocess
import sys

out = subprocess.run([sys.executable, "toc.py", "README.md"], capture_output=True, text=True)
assert out.returncode == 0 and "[Install](#install)" in out.stdout, out.stdout + out.stderr
print(out.stdout)
print("ok")
