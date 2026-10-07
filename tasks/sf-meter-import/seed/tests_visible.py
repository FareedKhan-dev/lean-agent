from meters.importer import total_kwh

with open("visible.csv", "w", encoding="utf-8") as f:
    f.write("meter_id,kwh\nm1,1.5\nm2,2.5\n")
assert abs(total_kwh("visible.csv") - 4.0) < 1e-9
print("ok")
