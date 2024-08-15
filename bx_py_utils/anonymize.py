import re
import string

_LOWERCASES = string.ascii_lowercase + 'äöüß'
_UPPERCASES = string.ascii_uppercase + 'ÄÖÜẞ'
_OTHER = ' ' + string.punctuation
_ANONYMIZATION_TRANS = str.maketrans(
    _LOWERCASES + _UPPERCASES + string.digits + _OTHER,
    'x' * len(_LOWERCASES) + 'X' * len(_UPPERCASES) + '#' * len(string.digits) + '_' * len(_OTHER)
)
_RE_OTHER = re.compile(r'[^xX_\.\s/-]')


def anonymize(value: str, handle_email: bool = True) -> str:
    """
    Anonymize the given string with special handling for eMail addresses.

    >>> anonymize('Foo Bar')
    'Fxx_Xxr'
    >>> anonymize('This is a Test 123 Foo Bar #+"-! End')
    'Txxx_xx_x_Xxxx_###_Xxx_Xxx_______Xxd'
    >>> anonymize('a.mail-address@test.tld')
    'a_xxxx_xxxxxxs@test.tld'
    >>> anonymize('a.mail-address@test.tld', handle_email=False)
    'a_xxxx_xxxxxxx_xxxx_xxd'
    """
    assert isinstance(value, str)

    if handle_email and '@' in value:
        value, at, domain = value.partition('@')
        if len(value) < 2:
            return value + at + domain

        return value[:1] + _RE_OTHER.sub('@', value[1:-1].translate(_ANONYMIZATION_TRANS)) + value[-1:] + at + domain

    value = f'{value[:1]}{value[1:-1].translate(_ANONYMIZATION_TRANS)}{value[-1:]}'
    return value


def anonymize_dict(
    data: dict,
    secret_keys: frozenset[str] = frozenset({'secret', 'password', 'token'}),  # These keys will be anonymized
) -> dict:
    """
    Returns a new dict with anonymized values for keys containing one of the given keywords.

    >>> anonymize_dict({'client_id': '123', 'client_secret': 'This is really secret'})
    {'client_id': '123', 'client_secret': 'Txxx_xx_xxxxxx_xxxxxt'}
    """
    anonymized_data = data.copy()  # Don't modify the original data!
    for key, value in anonymized_data.items():
        if value:
            if isinstance(value, str) and any(k in key.lower() for k in secret_keys):
                anonymized_data[key] = anonymize(value)
            elif isinstance(value, dict):
                anonymized_data[key] = anonymize_dict(value, secret_keys)
    return anonymized_data
