from shopfront.schemas.customer import CustomerSchema


class CustomerService:
    def __init__(self, customers):
        self.customers = customers
        self.schema = CustomerSchema()

    def register(self, data):
        customer = self.schema.load(data, self.customers.next_id())
        self.customers.add(customer)
        return customer

    def find_by_email(self, email):
        return self.customers.by_email(email)
