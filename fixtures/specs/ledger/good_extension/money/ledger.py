import threading
from datetime import date


class Ledger:
    """See SPEC.md."""

    def __init__(self):
        self._balances, self._history = {}, []
        self._limits, self._spent = {}, {}
        self._lock = threading.Lock()

    def open(self, account, balance=0):
        with self._lock:
            if account in self._balances:
                raise ValueError(f"account {account!r} exists")
            self._balances[account] = balance

    def balance(self, account):
        with self._lock:
            return self._balances[account]

    def set_daily_limit(self, account, pence):
        with self._lock:
            self._limits[account] = pence

    def transfer(self, source, target, pence, day=None):
        if type(pence) is not int or pence <= 0:
            raise ValueError("the amount must be a positive whole number of pence")
        day = day or date.today().isoformat()
        with self._lock:
            if self._balances[source] < pence:
                raise ValueError(f"{source!r} has only {self._balances[source]} pence")
            spent = self._spent.get((source, day), 0)
            if source in self._limits and spent + pence > self._limits[source]:
                raise ValueError(f"{source!r} would pass its daily limit")
            self._balances[source] -= pence
            self._balances[target] += pence
            self._spent[(source, day)] = spent + pence
            self._history.append((source, target, pence))

    def history(self, account):
        with self._lock:
            return [h for h in self._history if account in h[:2]]
