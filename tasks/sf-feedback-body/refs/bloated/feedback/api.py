import json


class ValidationError(ValueError):
    pass


class Field:
    def __init__(self, name, required=True, default=None):
        self.name, self.required, self.default = name, required, default

    def clean(self, value):
        return value


class IntField(Field):
    def __init__(self, name, minimum, maximum, **kwargs):
        super().__init__(name, **kwargs)
        self.minimum, self.maximum = minimum, maximum

    def clean(self, value):
        if type(value) is not int or not self.minimum <= value <= self.maximum:
            raise ValidationError(f"{self.name} must be a whole number from {self.minimum} to {self.maximum}")
        return value


class StrField(Field):
    def clean(self, value):
        if not isinstance(value, str):
            raise ValidationError(f"{self.name} must be text")
        return value


class Schema:
    fields = ()

    def load(self, raw):
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValidationError("expected a JSON object")
        out = {}
        for f in self.fields:
            if f.name not in data:
                if f.required:
                    raise ValidationError(f"{f.name} is required")
                out[f.name] = f.default
                continue
            out[f.name] = f.clean(data[f.name])
        return out


class FeedbackSchema(Schema):
    fields = (IntField("rating", 1, 5), StrField("comment", required=False, default=""))


def parse_feedback(raw_body):
    """Raw JSON from the feedback form -> {'rating': int 1..5, 'comment': str}. ValueError if invalid."""
    return FeedbackSchema().load(raw_body)
