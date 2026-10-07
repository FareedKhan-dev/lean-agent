from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    email: str
    name: str
