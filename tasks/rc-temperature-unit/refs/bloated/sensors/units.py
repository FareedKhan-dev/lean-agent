from abc import ABC, abstractmethod


class Unit(ABC):
    symbol = ""

    @abstractmethod
    def to_celsius(self, value):
        ...


class Celsius(Unit):
    symbol = "C"

    def to_celsius(self, value):
        return value


class Kelvin(Unit):
    symbol = "K"

    def to_celsius(self, value):
        return value - 273.15


class Fahrenheit(Unit):
    symbol = "F"

    def to_celsius(self, value):
        return (value - 32) * 5 / 9


class UnitRegistry:
    def __init__(self):
        self._units = {}

    def register(self, unit):
        self._units[unit.symbol] = unit
        return self

    def get(self, symbol):
        if symbol not in self._units:
            raise ValueError(f"unknown unit {symbol!r}")
        return self._units[symbol]


REGISTRY = UnitRegistry().register(Celsius()).register(Kelvin()).register(Fahrenheit())


def to_celsius(value, unit):
    """Convert a reading to degrees Celsius."""
    return REGISTRY.get(unit).to_celsius(value)
