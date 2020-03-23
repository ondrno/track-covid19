import os
import re


def _interval_to_ms(value: int, unit: str) -> int:
    """Convert the value and unit into milliseconds, if the value is not within the
    valid range (30 min to 24 hours) then the default (4 hours) is used."""
    one_minute_in_ms = 60 * 1000
    one_hour_in_ms = 60 * one_minute_in_ms

    min_interval = 30 * one_minute_in_ms
    max_interval = 24 * one_hour_in_ms
    default_interval = 4 * one_hour_in_ms
    if unit == 'h':
        interval = value * one_hour_in_ms
    elif unit == 'm':
        interval = value * one_minute_in_ms
    else:
        raise ValueError("Invalid query interval unit={}".format(unit))
    if min_interval <= interval <= max_interval:
        return interval
    else:
        return default_interval


def get_query_interval() -> int:
    """ Read the env variable 'QUERY_INTERVAL' which determines how often the web sites should be queried.
    The time has to be specified with a value + modifier (m|h), e.g. 30m for 30 minutes

    Valid ranges: 30 minutes (30m) to 24 hours (24h)
    """
    interval = os.environ.get('QUERY_INTERVAL')
    if interval:
        m = re.match(r'(\d+)(m|h)', interval)
        if m:
            interval = _interval_to_ms(int(m.group(1)), m.group(2))
        else:
            raise ValueError("Invalid QUERY_INTERVAL format. Valid range: 30m to 12h")
    else:
        # get the default value if specified value is too low
        interval = _interval_to_ms(0, 'm')

    return interval
