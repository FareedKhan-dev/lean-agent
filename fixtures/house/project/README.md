# shopfront

A small order service, structured the way the team structures everything:

- `models/`        plain dataclasses, no behaviour beyond small helpers
- `schemas/`       validation: every input is turned into a model by a schema
- `repositories/`  storage: one repository per model, all sharing `BaseRepository`
- `services/`      business logic: services use repositories, never storage directly
- `api/handlers.py` the functions the web layer calls; they return plain dicts
- `container.py`   builds the services and repositories and wires them together

When you add a feature, follow the same layering. Run `python tests_visible.py` before
you push.
