from _hidden_kit import check, load, raises, report

Ledger = load("money.ledger").Ledger


def daily_limit():
    led = Ledger()
    led.open("a", 10_000)
    led.open("b")
    led.set_daily_limit("a", 1000)
    led.transfer("a", "b", 600, day="2026-03-01")
    over = raises(lambda: led.transfer("a", "b", 500, day="2026-03-01"), ValueError)
    led.transfer("a", "b", 400, day="2026-03-01")
    led.transfer("a", "b", 900, day="2026-03-02")          # a new day starts a new allowance
    return over and led.balance("b") == 1900 and led.balance("a") == 8100


correct = check("a daily limit applies per day and refuses the excess", daily_limit)
report(correct)
