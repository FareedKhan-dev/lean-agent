from sensors.alerts import check_alert

assert check_alert({"sensor": "greenhouse-1", "value": 36.0, "unit": "C"})
assert not check_alert({"sensor": "greenhouse-1", "value": 20.0, "unit": "C"})
print("ok")
