"""Stock levels. Every change to stock goes through this module."""
import logging

log = logging.getLogger(__name__)

STOCK = {}


class StockError(Exception):
    """Base class for stock errors."""


class InsufficientStockError(StockError):
    def __init__(self, sku, available, requested):
        super().__init__(f"only {available} of {sku} in stock, {requested} requested")
        self.sku, self.available, self.requested = sku, available, requested


class InvalidQuantityError(StockError):
    pass


class StockGuard:
    """Checks every stock movement before it happens."""

    def __init__(self, stock):
        self.stock = stock

    def validate_quantity(self, qty):
        if not isinstance(qty, int) or qty < 0:
            raise InvalidQuantityError(f"bad quantity: {qty!r}")

    def ensure_available(self, sku, qty):
        available = self.stock.get(sku, 0)
        if qty > available:
            log.warning("refused take of %s x%s (have %s)", sku, qty, available)
            raise InsufficientStockError(sku, available, qty)


_guard = StockGuard(STOCK)


def set_stock(sku, qty):
    STOCK[sku] = qty


def level(sku):
    return STOCK.get(sku, 0)


def _take(sku, qty):
    """Remove qty units of sku from stock."""
    _guard.validate_quantity(qty)
    _guard.ensure_available(sku, qty)
    STOCK[sku] = level(sku) - qty


def _put(sku, qty):
    _guard.validate_quantity(qty)
    STOCK[sku] = level(sku) + qty
