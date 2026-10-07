def to_celsius(value, unit):
    """Convert a reading to degrees Celsius. unit is 'C', 'K' or 'F'."""
    if unit == "C":
        return value
    if unit == "K":
        return value - 273.15
    if unit == "F":
        return (value - 32) * 5 / 9
    raise ValueError(f"unknown unit {unit!r}")
