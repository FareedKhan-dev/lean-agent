from sensors.calibration import corrected
from sensors.units import to_celsius

LIMIT_C = 35.0


def check_alert(reading):
    """reading = {'sensor': id, 'value': number, 'unit': 'C' | 'K'}. True if it is too hot."""
    return corrected(reading["sensor"], to_celsius(reading["value"], reading["unit"])) > LIMIT_C
