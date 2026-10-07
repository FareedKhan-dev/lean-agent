import subprocess
import sys

out = subprocess.run([sys.executable, "report.py"], capture_output=True, text=True).stdout
assert "kettle" in out and "9 units" in out, out
print("ok")
