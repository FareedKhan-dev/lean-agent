from shopfront.models.customer import Customer


class CustomerSchema:
    """Turns submitted customer data into a Customer."""

    def load(self, data, new_id):
        email = str(data.get("email", "")).strip()
        name = str(data.get("name", "")).strip()
        if "@" not in email:
            raise ValueError("email is not valid")
        if not name:
            raise ValueError("name is required")
        return Customer(new_id, email, name)
