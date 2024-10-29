import datetime
import sys


def parse_dt(dtstr):
    """
    Helper for easy generate a `datetime` instance via string.

    >>> parse_dt(None) is None
    True
    >>> parse_dt('2020-01-01T00:00:00+0000')
    datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    >>> parse_dt('2020-01-02T03:04:05.678901+00:00')
    datetime.datetime(2020, 1, 2, 3, 4, 5, 678901, tzinfo=datetime.timezone.utc)
    """
    if dtstr is None:
        return None

    try:
        return datetime.datetime.fromisoformat(dtstr)
    except ValueError:
        if sys.version_info[:2] == (3, 10):
            # Python 3.10 supports only formats emitted by date.isoformat() or datetime.isoformat() :(
            return datetime.datetime.strptime(dtstr, '%Y-%m-%dT%H:%M:%S%z')
        raise
