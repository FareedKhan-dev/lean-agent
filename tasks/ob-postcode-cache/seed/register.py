"""The national postcode register. Owned by the data team: do not change this file."""
import time

DISTRICTS = {
    "SW1A1AA": "Westminster",
    "M11AE": "Manchester",
    "EH11YZ": "Edinburgh",
    "CF101BH": "Cardiff",
    "BT11AA": "Belfast",
}
SCANS = 0


def scan(code):
    """Look a normalised postcode up in the register. Slow: it reads the whole register."""
    global SCANS
    SCANS += 1
    time.sleep(0.05)
    return DISTRICTS.get(code)
