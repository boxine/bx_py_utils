import datetime


def parse_dt(dtstr):
    """
    Helper for easy generate a `datetime` instance via string.

    >>> parse_dt(None) is None
    True
    >>> parse_dt('2020-01-01T00:00:00+0000')
    datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    """
    if dtstr is None:
        return None
    return datetime.datetime.strptime(dtstr, '%Y-%m-%dT%H:%M:%S%z')
