"""Radio link to the field sensor. Owned by the hardware team: do not change this file."""
import random

SCRIPT = None      # tests set this to a list of results to replay
FETCHES = 0


def fetch():
    """Read one raw value from the sensor. Raises TimeoutError when the radio drops out."""
    global FETCHES
    FETCHES += 1
    if SCRIPT is not None:
        item = SCRIPT.pop(0)
        if isinstance(item, Exception):
            raise item
        return item
    if random.random() < 0.2:
        raise TimeoutError("radio link dropped")
    return "21.5"
