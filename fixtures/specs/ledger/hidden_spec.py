import random
import threading

from _hidden_kit import check, load, raises, report

Ledger = load("money.ledger").Ledger


def basics():
    led = Ledger()
    led.open("a", 1000)
    led.open("b")
    led.transfer("a", "b", 300)
    return (led.balance("a"), led.balance("b")) == (700, 300) and raises(lambda: led.open("a"), ValueError) \
        and raises(lambda: led.balance("zz"), KeyError)


def refusals():
    led = Ledger()
    led.open("a", 100)
    led.open("b", 0)
    bad = [lambda: led.transfer("a", "b", 101), lambda: led.transfer("a", "b", 0), lambda: led.transfer("a", "b", -5),
           lambda: led.transfer("a", "b", 2.5), lambda: led.transfer("a", "b", True)]
    return all(raises(f, ValueError) for f in bad) and (led.balance("a"), led.balance("b")) == (100, 0) and led.history("a") == []


def history():
    led = Ledger()
    for name in "abc":
        led.open(name, 500)
    led.transfer("a", "b", 10)
    led.transfer("c", "a", 20)
    led.transfer("b", "c", 5)
    return led.history("a") == [("a", "b", 10), ("c", "a", 20)] and led.history("b") == [("a", "b", 10), ("b", "c", 5)]


def concurrency():
    led = Ledger()
    names = ["w", "x", "y", "z"]
    for n in names:
        led.open(n, 10_000)

    def worker(seed):
        rng = random.Random(seed)
        for _ in range(400):
            s, t = rng.sample(names, 2)
            try:
                led.transfer(s, t, rng.randint(1, 900))
            except ValueError:
                pass

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    balances = [led.balance(n) for n in names]
    return sum(balances) == 40_000 and min(balances) >= 0


correct = all([check("open, balance, transfer", basics), check("bad transfers are refused and change nothing", refusals),
               check("history, oldest first", history), check("eight threads, no money created or lost", concurrency)])
report(correct)
