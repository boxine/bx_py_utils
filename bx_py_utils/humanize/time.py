import datetime


TIMESINCE_CHUNKS = (
    (60 * 60 * 24 * 365, '%.1f\xa0years'),
    (60 * 60 * 24 * 30, '%.1f\xa0months'),
    (60 * 60 * 24 * 7, '%.1f\xa0weeks'),
    (60 * 60 * 24, '%.1f\xa0days'),
    (60 * 60, '%.1f\xa0hours'),
    (60, '%.1f\xa0minutes'),
)


def human_timedelta(t):
    """
    Converts a time duration into a friendly text representation.

    >>> human_timedelta(0.001)
    '1.0\xa0ms'
    >>> human_timedelta(0.01)
    '10.0\xa0ms'
    >>> human_timedelta(0.9)
    '900.0\xa0ms'
    >>> human_timedelta(1)
    '1.0\xa0seconds'
    >>> human_timedelta(65.5)
    '1.1\xa0minutes'
    >>> human_timedelta(59 * 60)
    '59.0\xa0minutes'
    >>> human_timedelta(1.05*60*60)
    '1.1\xa0hours'
    >>> human_timedelta(24*60*60)
    '1.0\xa0days'
    >>> human_timedelta(2.54 * 60 * 60 * 24 * 365)
    '2.5\xa0years'
    """
    if isinstance(t, datetime.timedelta):
        t = t.total_seconds()
    assert isinstance(t, (int, float))

    if abs(t) < 1:
        return f'{round(t * 1000, 1):.1f}\xa0ms'
    if abs(t) < 60:
        return f'{round(t, 1):.1f}\xa0seconds'

    for seconds, time_string in TIMESINCE_CHUNKS:
        count = t / seconds
        if abs(count) >= 1:
            count = round(count, 1)
            break

    return time_string % count
