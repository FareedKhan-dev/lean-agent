# Ledger

`Ledger` in `money/ledger.py` keeps account balances in whole pence.

- `open(account, balance=0)` creates an account; opening one that exists raises ValueError.
- `balance(account)` returns its balance; an unknown account raises KeyError.
- `transfer(source, target, pence)` moves money between two accounts. The amount must be a positive whole number of pence (not a bool, not a float). A transfer that would take the source below zero raises ValueError and changes nothing.
- Transfers may run from many threads at once: no money may be created or lost, and no balance may go below zero.
- `history(account)` returns the transfers into or out of the account, oldest first, as `(source, target, pence)` tuples.
