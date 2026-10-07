import csv

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

    def export_csv(self, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["order id", "customer email", "total pence"])
            for o in sorted(self.orders.all(), key=lambda o: o.id):
                writer.writerow([o.id, self.customers.get(o.customer_id).email, o.total_pence()])
