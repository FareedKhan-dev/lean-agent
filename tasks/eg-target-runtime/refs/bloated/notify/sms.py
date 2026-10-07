from dataclasses import dataclass, field
from typing import Callable, Iterator, List, Optional, Sequence

from notify import gateway


@dataclass
class DeliveryReport:
    requests: int = 0
    numbers: int = 0
    failures: List[str] = field(default_factory=list)


class Chunker:
    def __init__(self, size: int):
        if size < 1:
            raise ValueError("size must be at least 1")
        self.size = size

    def split(self, items: Sequence[str]) -> Iterator[Sequence[str]]:
        for start in range(0, len(items), self.size):
            yield items[start:start + self.size]


class SmsDispatcher:
    def __init__(self, send: Callable = gateway.send, chunker: Optional[Chunker] = None):
        self.send = send
        self.chunker = chunker or Chunker(gateway.LIMIT)

    def dispatch(self, numbers: Sequence[str], message: str) -> DeliveryReport:
        report = DeliveryReport()
        for group in self.chunker.split(numbers):
            self.send(list(group), message)
            report.requests += 1
            report.numbers += len(group)
        return report


def send_all(numbers, message):
    """Text `message` to every number in `numbers` (a list), at most 50 per gateway request."""
    SmsDispatcher().dispatch(numbers, message)
