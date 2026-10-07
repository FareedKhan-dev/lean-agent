BUDGET = {"travel": 400, "food": 250, "office": 120}


def over_budget(totals):
    return sorted(c for c, spent in totals.items() if spent > BUDGET.get(c, 0))
