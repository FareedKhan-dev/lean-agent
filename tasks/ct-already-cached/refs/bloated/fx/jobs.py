from fx.convert import clear_rate_cache
from fx.rates import rate


def after_rates_update():
    """Run by the scheduler as soon as the rates service publishes the 06:00 rates."""
    rate.cache_clear()
    clear_rate_cache()
