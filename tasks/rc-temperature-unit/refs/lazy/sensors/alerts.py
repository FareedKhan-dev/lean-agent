from sensors.calibration import corrected
from sensors.units import to_celsius

LIMIT_C = 35.0


def check_alert(reading):
    """reading = {'sensor': id, 'value': number, 'unit': 'C' | 'K' | 'F'}. True if it is too hot."""
    value, unit = reading["value"], reading["unit"]
    if unit == "F":
        value, unit = (value - 32) * 5 / 9, "C"
    return corrected(reading["sensor"], to_celsius(value, unit)) > LIMIT_C
