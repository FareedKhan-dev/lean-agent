from shopfront.schemas.order import OrderSchema


class OrderService:
    def __init__(self, orders, customers):
        self.orders = orders
        self.customers = customers
        self.schema = OrderSchema()

    def place(self, data):
        order = self.schema.load(data, self.orders.next_id())
        if self.customers.get(order.customer_id) is None:
            raise ValueError("no such customer")
        self.orders.add(order)
        return order

    def orders_for(self, customer_id):
        return self.orders.for_customer(customer_id)
