import threading


class Ledger:
    """See SPEC.md."""

    def __init__(self):
        self._balances, self._history = {}, []
        self._lock = threading.Lock()

    def open(self, account, balance=0):
        with self._lock:
            if account in self._balances:
                raise ValueError(f"account {account!r} exists")
            self._balances[account] = balance

    def balance(self, account):
        with self._lock:
            return self._balances[account]

    def transfer(self, source, target, pence):
        if type(pence) is not int or pence <= 0:
            raise ValueError("the amount must be a positive whole number of pence")
        with self._lock:
            if self._balances[source] < pence:
                raise ValueError(f"{source!r} has only {self._balances[source]} pence")
            self._balances[source] -= pence
            self._balances[target] += pence
            self._history.append((source, target, pence))

    def history(self, account):
        with self._lock:
            return [h for h in self._history if account in h[:2]]
