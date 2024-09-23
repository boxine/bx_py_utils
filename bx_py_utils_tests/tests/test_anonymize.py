import unittest

from parameterized import parameterized

from bx_py_utils.anonymize import anonymize_dict


class TestAnonymizeDict(unittest.TestCase):
    def test_anonymize_dict(self):
        data = {
            'something': 'Untouched value!',
            'client_secret': 'A test secret',
            'PassWord': 'This is a password!',
            'Token': 'Foo Bar Baz',
            'sub-dict': {
                'token': 'Not really a token!',
            },
        }
        self.assertEqual(
            anonymize_dict(data),
            {
                'something': 'Untouched value!',
                'client_secret': 'A_xxxx_xxxxxt',
                'PassWord': 'Txxx_xx_x_xxxxxxxx!',
                'Token': 'Fxx_Xxx_Xxz',
                'sub-dict': {
                    'token': 'Nxx_xxxxxx_x_xxxxx!',
                },
            },
        )
        # The origin, mutable dict is unchanged:
        self.assertEqual(
            data,
            {
                'something': 'Untouched value!',
                'client_secret': 'A test secret',
                'PassWord': 'This is a password!',
                'Token': 'Foo Bar Baz',
                'sub-dict': {
                    'token': 'Not really a token!',
                },
            },
        )

    @parameterized.expand(
        [
            ('Authorization', 'Authorization'),
            ('Authorization', 'authorization'),
            ('authorization', 'Authorization'),
            ('authorization', 'authorization'),
            ('UserAuthorization', 'Authorization'),
            ('UserAuthorization', 'authorization'),
            ('user_authorization', 'Authorization'),
            ('user_authorization', 'authorization'),
        ]
    )
    def test_anonymize_dict_ignore_case(self, key, secret_key):
        data = {
            'lang': 'es',
            key: 'secret',
        }
        self.assertEqual(
            anonymize_dict(data, frozenset({secret_key})),
            {
                'lang': 'es',
                key: 'sxxxxt',
            },
        )

    def test_anonymize_dict_truncating_output(self):
        data = {
            'short_safe': 'SAFE',
            'short_secret': 'SECRET',
            'sub-dict': {
                'long_safe': 'qwertyuiopasdfghjklzxcvbnm',
                'long_secret': '0123456789012345678901234567890123456789',
            },
        }
        self.assertEqual(
            anonymize_dict(data, max_length=10),
            {
                'short_safe': 'SAFE',
                'short_secret': 'SXXXXT',
                'sub-dict': {
                    'long_safe': 'qwertyuiopasdfghjklzxcvbnm',
                    'long_secret': '0########…',
                },
            },
        )
        # The origin, mutable dict is unchanged:
        self.assertEqual(
            data,
            {
                'short_safe': 'SAFE',
                'short_secret': 'SECRET',
                'sub-dict': {
                    'long_safe': 'qwertyuiopasdfghjklzxcvbnm',
                    'long_secret': '0123456789012345678901234567890123456789',
                },
            },
        )
