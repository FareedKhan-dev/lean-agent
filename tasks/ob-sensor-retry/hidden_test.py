from _hidden_kit import check, load, no_sleep, report

no_sleep()
link = load("link")
sensor = load("sensor")


def run(script):
    link.SCRIPT, link.FETCHES = list(script), 0
    try:
        return ("ok", sensor.read_value(), link.FETCHES)
    except Exception as e:
        return (type(e).__name__, None, link.FETCHES)


drop = TimeoutError("radio link dropped")
correct = (check("a clean read returns the value", lambda: run(["21.5"]) == ("ok", 21.5, 1))
           and check("two drop-outs then a value: the value, after three reads",
                     lambda: run([drop, drop, "19.0"]) == ("ok", 19.0, 3))
           and check("three drop-outs: TimeoutError after exactly three reads",
                     lambda: run([drop, drop, drop]) == ("TimeoutError", None, 3)))
quality = check("bad data fails at once, without a retry",
                lambda: run(["garbage", "20.0", "20.0"]) == ("ValueError", None, 1))
report(correct, quality=quality)
