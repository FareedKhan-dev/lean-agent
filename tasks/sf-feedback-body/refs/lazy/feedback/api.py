import json


def parse_feedback(raw_body):
    """Raw JSON from the feedback form -> {'rating': int 1..5, 'comment': str}. ValueError if invalid."""
    data = json.loads(raw_body)
    return {"rating": int(data["rating"]), "comment": data.get("comment", "")}
