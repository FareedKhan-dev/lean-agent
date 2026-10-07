import subprocess
import sys

out = subprocess.run([sys.executable, "wordfreq.py", "sample.txt"], capture_output=True, text=True)
assert out.returncode == 0 and out.stdout.strip(), out.stderr
print(out.stdout)
print("ok")
