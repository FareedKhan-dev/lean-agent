"""Per-sensor corrections, measured against a reference thermometer when each sensor was installed."""

OFFSETS = {"greenhouse-1": -0.4, "greenhouse-2": 0.3, "us-yard-7": 1.1}


def corrected(sensor_id, celsius):
    return celsius + OFFSETS.get(sensor_id, 0.0)
