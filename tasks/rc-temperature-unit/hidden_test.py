from _hidden_kit import check, load, raises, report

alerts = load("sensors.alerts")
stats = load("sensors.stats")


def reading(value, unit, sensor="us-yard-7"):
    return {"sensor": sensor, "value": value, "unit": unit}


correct = (check("a hot Fahrenheit reading raises the alert", lambda: alerts.check_alert(reading(100, "F")) is True)
           and check("a mild Fahrenheit reading does not", lambda: alerts.check_alert(reading(80, "F")) is False)
           and check("Celsius and Kelvin still work", lambda: alerts.check_alert(reading(36.0, "C", "greenhouse-1"))
                     and not alerts.check_alert(reading(290.0, "K", "greenhouse-1")))
           and check("unknown units still fail loudly", lambda: raises(lambda: alerts.check_alert(reading(1, "X")), ValueError)))
quality = (check("the daily mean (never named in the report) handles Fahrenheit, with calibration",
                 lambda: abs(stats.daily_mean([reading(50, "F"), reading(68, "F")]) - 16.1) < 0.01)
           and check("calibration offsets are still applied to alerts",
                     lambda: alerts.check_alert(reading(34.5, "C", "us-yard-7")) is True))
report(correct, quality=quality)
