from _hidden_kit import check, find, load, report

parse = find(load("feedback.api"), "parse_feedback")


def refused(raw):
    """Must raise ValueError: anything else becomes a 500 instead of a 400."""
    try:
        parse(raw)
    except ValueError:
        return True
    except Exception:
        return False
    return False


correct = parse is not None and check("valid bodies", lambda: (
    parse('{"rating": 4, "comment": "great"}') == {"rating": 4, "comment": "great"}
    and parse('{"rating": 5}') == {"rating": 5, "comment": ""}
    and parse('{"rating": 1}') == {"rating": 1, "comment": ""}))
bad = ["null", "[]", '"5"', "not json", "{}", '{"rating": 9}', '{"rating": 6}', '{"rating": 0}', '{"rating": true}',
       '{"rating": "5"}', '{"rating": 4.5}', '{"rating": 4, "comment": 7}']
safe = check("every malformed body raises ValueError", lambda: all(refused(b) for b in bad))
report(correct, safe=safe)
