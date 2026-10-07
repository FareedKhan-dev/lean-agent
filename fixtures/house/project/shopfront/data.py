from shopfront.api.handlers import place_order, register_customer


def load_demo():
    register_customer({"email": "ann@example.org", "name": "Ann"})
    register_customer({"email": "Bo@Example.org", "name": "Bo"})
    for placed, sku, qty, price in (("2026-03-01", "kettle", 1, 2499), ("2026-03-04", "mug", 4, 650),
                                    ("2026-03-09", "teapot", 1, 3200), ("2026-03-11", "mug", 2, 650),
                                    ("2026-03-15", "tray", 1, 1800), ("2026-03-20", "kettle", 1, 2499),
                                    ("2026-03-22", "cups", 6, 400)):
        place_order({"customer_id": 1, "placed": placed, "lines": [{"sku": sku, "quantity": qty, "unit_pence": price}]})
    place_order({"customer_id": 2, "placed": "2026-03-05", "lines": [{"sku": "mug", "quantity": 1, "unit_pence": 650}]})
