from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trip:
    origin: str
    destination: str
    depart: datetime
    arrive: datetime
    price_pence: int
