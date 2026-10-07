from typing import List

DRIVERS = {"oban": ["07700900001", "07700900002"], "mallaig": ["07700900003"]}


def numbers_for(depot: str) -> List[str]:
    return DRIVERS.get(depot, [])
