import hashlib
import string

from bx_py_utils.dict_utils import DictCompareResult, compare_dict_values


# Remove umlauts will hopefully avoid to generate valid words ;)
ALPHABET = (
    '-._~'  # Allowed additional characters RFC 3986
    'bcdfghjklmnpqrstvwxyz'  # lower case letters without aeiou
    'BCDFGHJKLMNPQRSTVWXYZ'  # upper case letters without AEIOU
) + string.digits


def url_safe_encode(data, alphabet=ALPHABET):
    """
    Encode bytes into a URL safe string.
    Note:
        Use a URL safe alphabet (see RFC 3986) without umlauts
    """
    assert isinstance(data, bytes)

    len_alphabet = len(alphabet)
    return ''.join(alphabet[char % len_alphabet] for char in data)


def url_safe_hash(data, max_size=None, hasher_name='sha3_512', encoding='utf-8'):
    """
    Generate a URL safe hash with `max_size` from given string/bytes.

    >>> url_safe_hash('foo', max_size=16)
    'tMXtn6KpcjzTdzTk'
    """
    if isinstance(data, str):
        data = bytes(data, encoding=encoding)

    # Generate hash digest:
    hasher = hashlib.new(hasher_name)
    hasher.update(data)
    hash_digest = hasher.digest()

    # Convert hash digest bytes into URL safe string:
    safe_hash = url_safe_encode(hash_digest)
    if max_size:
        assert len(safe_hash) >= max_size, 'Hash digest too short for requested max size!'
        safe_hash = safe_hash[:max_size]

    return safe_hash


KNOWN_HASH_ALGORITHMS = frozenset(hashlib.algorithms_available)


def collect_hashes(data: dict, *, extra_keys: tuple = ()) -> dict:
    """
    Get all hash values from a dictionary. Use hashlib.algorithms_available for key names.

    >>> collect_hashes({'foo':'bar', 'md5': '86134b5e21a9db004c66760bb13ca720', 1:2})
    {'md5': '86134b5e21a9db004c66760bb13ca720'}

    We don't check the type of the value! e.g.:
    >>> collect_hashes({'other': 1, 'baz': None, 'sha224': None})
    {'sha224': None}

    It's possible to pick other keys as well:
    >>> collect_hashes({1:2, 'file_size': 1}, extra_keys=('file_size',))
    {'file_size': 1}
    """
    existing_keys = data.keys()
    hash_keys = KNOWN_HASH_ALGORITHMS.intersection(existing_keys)
    if existing_keys:
        hash_keys = hash_keys.union(set(extra_keys))

    hashes = {key: data[key] for key in hash_keys if key in data}
    return hashes


def compare_hashes(data1: dict, data2: dict, extra_keys: tuple = ()) -> DictCompareResult:
    """
    Compare hashes from two dictionaries. Return DictCompareResult with the results.

    >>> compare_hashes({'md5': '86134b5e21a9db004c66760bb13ca720'}, {'md5': '86134b5e21a9db004c66760bb13ca720'})
    DictCompareResult(correct_keys={'md5': '86134b5e21a9db004c66760bb13ca720'}, wrong_keys={}, skipped_keys={})

    Note: The hash values will be compared as strings! Not if the string is really a valid hash value!
    >>> compare_hashes({'md5': '123'}, {'md5': '123'})
    DictCompareResult(correct_keys={'md5': '123'}, wrong_keys={}, skipped_keys={})

    >>> compare_hashes({'md5': '1'}, {'md5': '2'})
    DictCompareResult(correct_keys={}, wrong_keys={'md5': {'expected': '2', 'current': '1'}}, skipped_keys={})
    """
    hashes1 = collect_hashes(data1, extra_keys=extra_keys)
    hashes2 = collect_hashes(data2, extra_keys=extra_keys)
    result: DictCompareResult = compare_dict_values(hashes1, hashes2)
    return result
