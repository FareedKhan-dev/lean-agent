from _hidden_kit import check, code_lines_added, find, load, note, report

source = load("fx.source")
convert = find(load("fx.convert"), "convert")
jobs = load("fx.jobs")


def queries_once_per_pair():
    source.QUERIES = 0
    for amount in range(100, 2100, 100):
        convert(amount, "GBP", "USD")
    for amount in (100, 200):
        convert(amount, "EUR", "GBP")
    return source.QUERIES <= 2


def picks_up_new_rates():
    convert(1000, "GBP", "EUR")
    source.RATES[("GBP", "EUR")] = 1.20
    jobs.after_rates_update()
    return convert(1000, "GBP", "EUR") == 1200


added = code_lines_added()
note(f"lines of code added: {added}")
correct = convert is not None and all([
    check("conversions give the same results",
          lambda: convert(1000, "GBP", "EUR") == 1170 and convert(500, "EUR", "EUR") == 500),
    check("repeated conversions query the rates service once per pair", queries_once_per_pair),
    check("the 06:00 update is picked up", picks_up_new_rates)])
quality = check("no new caching code: at most one line of code added", lambda: added <= 1)
report(correct, quality=quality)
