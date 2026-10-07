from inventory import core, orders

core.set_stock("kettle", 10)
orders.reserve([("kettle", 3)])
assert core.level("kettle") == 7
print("ok")
