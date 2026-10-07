from shopfront.models.order import Order, OrderLine


class OrderSchema:
    """Turns submitted order data into an Order."""

    def load(self, data, new_id):
        lines = [OrderLine(str(l["sku"]), int(l["quantity"]), int(l["unit_pence"])) for l in data.get("lines", [])]
        if not lines:
            raise ValueError("an order needs at least one line")
        return Order(new_id, int(data["customer_id"]), str(data["placed"]), lines)
