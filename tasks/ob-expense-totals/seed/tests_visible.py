from expenses import totals_by_category

with open("visible.csv", "w", encoding="utf-8") as f:
    f.write("date,category,amount\n2026-03-02,travel,12.50\n2026-03-03,travel,7.50\n")
assert totals_by_category("visible.csv")["travel"] == 20
print("ok")
