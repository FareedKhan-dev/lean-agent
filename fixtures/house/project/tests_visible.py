from shopfront.api.handlers import list_orders, place_order, register_customer

register_customer({"email": "cy@example.org", "name": "Cy"})
place_order({"customer_id": 1, "placed": "2026-04-01", "lines": [{"sku": "mug", "quantity": 2, "unit_pence": 650}]})
assert list_orders(1)[0]["total_pence"] == 1300
print("ok")
