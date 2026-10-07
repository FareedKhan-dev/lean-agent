def to_celsius(value, unit):
    """Convert a reading to degrees Celsius. unit is 'C' or 'K'."""
    if unit == "C":
        return value
    if unit == "K":
        return value - 273.15
    raise ValueError(f"unknown unit {unit!r}")
