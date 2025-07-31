from __future__ import annotations

import dataclasses
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


@dataclasses.dataclass
class DictCompareResult:
    correct_keys: dict  # Values of keys are present and equal in both dicts
    wrong_keys: dict  # Values of keys are present, but not equal
    skipped_keys: dict  # Keys are not present in one of the dicts

    def compare_successful(self) -> bool | None:
        if not self.correct_keys and not self.wrong_keys:
            # Nothing compared -> undefined if the compare are ok or not
            return None

        if self.correct_keys and not self.wrong_keys:
            return True
        else:
            return False


def compare_dict_values(dict1: dict, dict2: dict) -> DictCompareResult:
    """
    Compare two dictionaries if values of the same keys are present and equal.

    >>> compare_dict_values({'a': 1}, {'a': 1, 'c': 2})
    DictCompareResult(correct_keys={'a': 1}, wrong_keys={}, skipped_keys={'c': {'expected': 2, 'current': None}})

    >>> compare_dict_values({'a': 0}, {'a': 1})
    DictCompareResult(correct_keys={}, wrong_keys={'a': {'expected': 1, 'current': 0}}, skipped_keys={})

    The key must be present in both:
    >>> compare_dict_values({'a': None}, {})
    DictCompareResult(correct_keys={}, wrong_keys={}, skipped_keys={'a': {'expected': None, 'current': None}})
    >>> compare_dict_values({}, {'a': 0})
    DictCompareResult(correct_keys={}, wrong_keys={}, skipped_keys={'a': {'expected': 0, 'current': None}})

    Comapre 0 or False or None on both sides is successful:
    >>> compare_dict_values({'a': 0}, {'a': 0})
    DictCompareResult(correct_keys={'a': 0}, wrong_keys={}, skipped_keys={})
    >>> compare_dict_values({'a': False}, {'a': False})
    DictCompareResult(correct_keys={'a': False}, wrong_keys={}, skipped_keys={})
    >>> compare_dict_values({'a': None}, {'a': None})
    DictCompareResult(correct_keys={'a': None}, wrong_keys={}, skipped_keys={})

    We also check the types, e.g.: 1 is not equal to True:
    >>> compare_dict_values({'a': 1}, {'a': True})
    DictCompareResult(correct_keys={}, wrong_keys={'a': {'expected': True, 'current': 1}}, skipped_keys={})
    """
    key_union = sorted(dict1.keys() | dict2.keys())
    correct_keys = {}
    wrong_keys = {}
    skipped_keys = {}
    for key in key_union:
        expected_value = dict2.get(key)
        current_value = dict1.get(key)
        if key not in dict1 or key not in dict2:
            skipped_keys[key] = {'expected': expected_value, 'current': current_value}
        elif type(expected_value) == type(current_value) and expected_value == current_value:  # noqa: E721
            correct_keys[key] = expected_value
        else:
            wrong_keys[key] = {'expected': expected_value, 'current': current_value}

    result = DictCompareResult(
        correct_keys=correct_keys,
        wrong_keys=wrong_keys,
        skipped_keys=skipped_keys,
    )
    return result
