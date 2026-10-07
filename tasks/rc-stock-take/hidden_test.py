from _hidden_kit import check, load, raises, report

core = load("inventory.core")
orders = load("inventory.orders")
shipping = load("inventory.shipping")


def fresh(**levels):
    core.STOCK.clear()
    core.STOCK.update(levels)


def reserve_ok():
    fresh(kettle=10, mixer=4)
    orders.reserve([("kettle", 3), ("mixer", 4)])
    return core.level("kettle") == 7 and core.level("mixer") == 0


def reserve_too_much():
    fresh(kettle=2)
    return raises(lambda: orders.reserve([("kettle", 5)])) and core.level("kettle") == 2


def dispatch_too_much():
    fresh(toaster=1)
    return raises(lambda: shipping.dispatch("toaster", 3)) and core.level("toaster") == 1


correct = check("a normal order reserves stock", reserve_ok) and check("an order for too much raises and changes nothing", reserve_too_much)
quality = (check("the warehouse scanner cannot overdraw either (same shared path)", dispatch_too_much)
           and check("dispatching what we have still works", lambda: (fresh(toaster=3), shipping.dispatch("toaster", 3), core.level("toaster"))[2] == 0))
report(correct, quality=quality)
