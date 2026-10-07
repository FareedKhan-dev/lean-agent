from shopfront.repositories.base import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self):
        self._items = {}

    def add(self, item):
        self._items[item.id] = item

    def get(self, item_id):
        return self._items.get(item_id)

    def all(self):
        return list(self._items.values())

    def for_customer(self, customer_id):
        """A customer's orders, oldest first."""
        return sorted((o for o in self._items.values() if o.customer_id == customer_id), key=lambda o: (o.placed, o.id))
