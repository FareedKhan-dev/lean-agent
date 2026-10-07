import link
import sensor

link.SCRIPT = [TimeoutError("drop"), "20.0"]
assert sensor.read_value() == 20.0
print("ok")
