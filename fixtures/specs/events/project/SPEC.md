# Event dispatcher

`Dispatcher` in `events/dispatcher.py` delivers events to subscribers inside this process.

- `subscribe(topic, handler)` registers a handler (a callable that takes the payload) and returns a subscription id.
- `unsubscribe(subscription_id)` removes that subscription; an unknown id is ignored.
- `publish(topic, payload)` calls every handler subscribed to `topic`, in the order they subscribed, then every handler subscribed to `"*"` (all topics), and returns how many handlers it called.
- A handler that raises must not stop the others. `publish` still calls the rest, then raises `DeliveryError`, whose `errors` attribute lists `(subscription_id, exception)` for each failure.
- A handler may subscribe or unsubscribe while an event is being delivered; the change applies from the next `publish`.
