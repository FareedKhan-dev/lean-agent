from _hidden_kit import check, load, raises, report

handlers = load("shopfront.api.handlers")
load("shopfront.data").load_demo()
place = handlers.place_order
line = lambda q: {"customer_id": 1, "placed": "2026-04-02", "lines": [{"sku": "mug", "quantity": q, "unit_pence": 650}]}
correct = check("zero and negative quantities are refused, positive ones accepted",
                lambda: raises(lambda: place(line(0)), ValueError) and raises(lambda: place(line(-2)), ValueError)
                and place(line(3))["total_pence"] == 1950)
report(correct)
