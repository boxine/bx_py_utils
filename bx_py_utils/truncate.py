def truncate(value: str, length: int) -> str:
    """
    Truncates the given string to the given length

    >>> truncate('foo bar', 3)
    'fo…'
    >>> truncate('foo bar', 100)
    'foo bar'
    >>> truncate('foo bar', 1)
    '…'
    >>> truncate('foo bar', 0)
    Traceback (most recent call last):
        ...
    ValueError: length must be greater than 0
    >>> truncate('foo bar', -1)
    Traceback (most recent call last):
        ...
    ValueError: length must be greater than 0
    """
    assert isinstance(value, str)
    assert isinstance(length, int)

    if length <= 0:
        raise ValueError('length must be greater than 0')

    return value if len(value) <= length else f'{value[:length - 1]}…'
