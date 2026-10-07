from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """Storage for one kind of model."""

    @abstractmethod
    def add(self, item):
        ...

    @abstractmethod
    def get(self, item_id):
        ...

    @abstractmethod
    def all(self):
        ...

    def next_id(self):
        return max((item.id for item in self.all()), default=0) + 1
