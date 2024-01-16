from __future__ import annotations

import hashlib
import re
import unicodedata
from uuid import UUID


def levenshtein_distance(word1: str, word2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings.

    >>> levenshtein_distance('planet', 'planetary')
    3
    >>> levenshtein_distance('book', 'back')
    2
    >>> levenshtein_distance('book', 'book')
    0
    """
    if len(word1) < len(word2):
        return levenshtein_distance(word2, word1)

    if len(word2) == 0:
        return len(word1)

    previous_row = range(len(word2) + 1)

    for i, c1 in enumerate(word1):
        current_row = [i + 1]
        for j, c2 in enumerate(word2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def get_words(text, min_word_length=0, ignore_words=(), to_lower=True):
    """
    Extract words from a text. With filter functionality.

    >>> get_words('test Äöüß!')
    ['test', 'äöüß']
    >>> get_words('12 123 1234', min_word_length=3)
    ['123', '1234']
    >>> get_words('A AB cd EfG hij', min_word_length=2, ignore_words=('ab', 'efg'))
    ['cd', 'hij']
    """
    if to_lower:
        text = text.lower()
    text = unicodedata.normalize('NFKC', text)

    text = re.sub(r'[^\w\s-]', '', text).strip()
    words = text.split(' ')

    if min_word_length > 0:
        words = [word for word in words if len(word) >= min_word_length]

    if ignore_words:
        words = [word for word in words if word not in ignore_words]

    return words


def compare_sentences(text1, text2, min_word_length=4, ignore_words=(), compare_lower=True) -> None | int:
    """
    Calculates the Levenshtein distance between text1 and text2. With filter functionality.
    But split to words and ignore special characters.

    >>> compare_sentences('planet', 'planetary')
    3
    >>> compare_sentences('orchestration', 'container')
    10
    >>> compare_sentences('This is the SAME!', 'this is the same')
    0
    """
    if text1 and text2 and text1 == text2:
        return 0

    text1 = ' '.join(get_words(text1, min_word_length, ignore_words, to_lower=compare_lower))
    text2 = ' '.join(get_words(text2, min_word_length, ignore_words, to_lower=compare_lower))

    if not text1 or not text2:
        return None

    return levenshtein_distance(text1, text2)


def uuid_from_text(text: str) -> UUID:
    """
    Generate a UUID instance from the given text in a determinism may via SHA224 hash.

    >>> uuid_from_text('foo')
    UUID('0808f64e-60d5-8979-fcb6-76c96ec93827')
    """
    assert isinstance(text, str)
    hexdigest = hashlib.sha224(bytes(text, encoding='utf-8')).hexdigest()
    uuid = UUID(hexdigest[:32])
    return uuid


def ensure_lf(text: str | None) -> str | None:
    """
    Replace line endings to unix-style.

    >>> ensure_lf('foo\\r\\nbar\\rbaz')
    'foo\\nbar\\nbaz'
    """
    if text and '\r' in text:
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
    return text


def startswith_prefixes(text: str | None, prefixes: tuple[str, ...]) -> bool:
    """
    >>> startswith_prefixes('foobar', prefixes=('foo','bar'))
    True
    >>> startswith_prefixes('barfoo', prefixes=('foo','bar'))
    True
    >>> startswith_prefixes(' barfoo', prefixes=('foo','bar'))
    True
    >>> startswith_prefixes('no match', prefixes=('foo','bar'))
    False
    """
    if text:
        text = text.lstrip()
        for prefix in prefixes:
            if text.startswith(prefix):
                return True
    return False
