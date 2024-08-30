from __future__ import annotations

import re
from collections.abc import Generator, Iterable
from typing import Any


def dict_get(item, *keys) -> None | bool | str | dict | list:
    """
    nested dict `get()`

    >>> example={1: {2: 'X'}}
    >>> dict_get(example, 1, 2)
    'X'
    >>> dict_get(example, 1)
    {2: 'X'}
    >>> dict_get(example, 1, 2, 3) is None
    True
    >>> dict_get(example, 'foo', 'bar') is None
    True
    >>> dict_get('no dict', 'no key') is None
    True
    """
    for key in keys:
        if isinstance(item, dict):
            item = item.get(key)
        else:
            return None
    return item


def pluck(obj: dict, keys: Iterable[str]):
    """
    Extract values from a dict, if they are present

    >>> pluck({'a': 1, 'b': 2}, ['a', 'c'])
    {'a': 1}
    """
    assert isinstance(obj, dict)
    res = {}
    for k in keys:
        if k in obj:
            res[k] = obj[k]
    return res


def dict_list2markdown(data: Iterable[dict]) -> Generator[str]:
    """
    Convert a list of dictionaries into a markdown table.
    It's assumed that all dictionaries have the same keys.
    It's without cell width normalisation. (Use the great "tabulate" library for this)

    >>> result=dict_list2markdown([{'a': 'A1', 'b': 'B1'}, {'a': 'A2', 'b': 'B2'}, {'a': 'A3', 'b': 'B3'}])
    >>> print('\\n'.join(result))
    | index | a | b |
    | ----- | ----- | ----- |
    | 1 | A1 | B1 |
    | 2 | A2 | B2 |
    | 3 | A3 | B3 |
    """

    def to_cell_value(value: Any) -> str:
        value = str(value)
        value = re.sub(r'\r\n|\r|\n', '<br>', value)
        value = value.replace('|', r'\|')
        return value

    keys = None
    for index, entry in enumerate(data, start=1):
        if keys is None:
            keys = entry.keys()
            yield f'| index | {" | ".join(to_cell_value(key) for key in keys)} |'
            yield f'| ----- | {" | ".join(["-----"] * len(keys))} |'
        else:
            assert entry.keys() == keys, f'Entry {index} has different keys: {entry.keys()} != {keys}'
        row = ' | '.join(to_cell_value(entry[key]) for key in keys)
        yield f'| {index} | {row} |'
