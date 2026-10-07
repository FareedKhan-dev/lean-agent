from statistics import mean

from sensors.calibration import corrected
from sensors.units import to_celsius


def daily_mean(readings):
    """Mean corrected temperature in Celsius over one day's readings."""
    return mean(corrected(r["sensor"], to_celsius(r["value"], r["unit"])) for r in readings)
