from money.ledger import Ledger

led = Ledger()
led.open("a", 1000)
led.open("b")
led.transfer("a", "b", 250)
assert (led.balance("a"), led.balance("b")) == (750, 250)
print("ok")
