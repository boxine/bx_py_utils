import unittest

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
        self.assertEqual(data['PassWord'], 'This is a password!')
        self.assertEqual(data['sub-dict']['token'], 'Not really a token!')
