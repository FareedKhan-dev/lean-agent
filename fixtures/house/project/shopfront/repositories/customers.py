from shopfront.repositories.base import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self):
        self._items = {}

    def add(self, item):
        self._items[item.id] = item

    def get(self, item_id):
        return self._items.get(item_id)

    def all(self):
        return list(self._items.values())

    def by_email(self, email):
        return next((c for c in self._items.values() if c.email == email), None)
