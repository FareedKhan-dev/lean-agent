from _hidden_kit import check, load, report

handlers = load("shopfront.api.handlers")
load("shopfront.data").load_demo()
orders = handlers.SERVICES.orders
correct = check("orders are counted per customer", lambda: orders.count_for(1) == 7 and orders.count_for(2) == 1
                and orders.count_for(99) == 0)
report(correct)
