from shopfront.container import build

SERVICES = build()


def order_to_dict(order):
    return {"id": order.id, "placed": order.placed, "total_pence": order.total_pence(),
            "lines": [{"sku": l.sku, "quantity": l.quantity} for l in order.lines]}


def register_customer(payload):
    customer = SERVICES.customers.register(payload)
    return {"id": customer.id, "email": customer.email}


def place_order(payload):
    return order_to_dict(SERVICES.orders.place(payload))


def list_orders(customer_id):
    return [order_to_dict(o) for o in SERVICES.orders.orders_for(customer_id)]


def recent_orders(customer_id):
    return list_orders(customer_id)[::-1][:5]
