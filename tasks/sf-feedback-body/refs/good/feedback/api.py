import json


def parse_feedback(raw_body):
    """Raw JSON from the feedback form -> {'rating': int 1..5, 'comment': str}. ValueError if invalid."""
    data = json.loads(raw_body)
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    rating, comment = data.get("rating"), data.get("comment", "")
    if type(rating) is not int or not 1 <= rating <= 5:
        raise ValueError("rating must be a whole number from 1 to 5")
    if not isinstance(comment, str):
        raise ValueError("comment must be text")
    return {"rating": rating, "comment": comment}
