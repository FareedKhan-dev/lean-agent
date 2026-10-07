from sensor import read_value


def panel_text():
    return f"Field sensor: {read_value():.1f} C"
