from feedback.api import parse_feedback

assert parse_feedback('{"rating": 4, "comment": "great"}') == {"rating": 4, "comment": "great"}
print("ok")
