import urllib
import urllib.request
from unittest import TestCase
from unittest.mock import patch

import requests

from bx_py_utils.test_utils.deny_requests import DenyCallError, deny_any_real_request


class DenyAnyRealRequestTestCase(TestCase):
    def test_happy_path(self):

        # We must not activate DenyAnyRealRequestContextManager here, because it's always used in tests.
        # Activated in bx_py_utils_tests.tests.pre_configure_tests()

        with self.assertRaises(DenyCallError) as cm:
            urllib.request.urlopen('http://www.python.org/')
        self.assertIn('Deny socket create_connection() call', cm.exception.args[0])

        # requests used urllib3 ;)
        with self.assertRaises(DenyCallError) as cm:
            requests.get('http://www.python.org/')
        self.assertIn('Deny urllib3 create_connection() call', cm.exception.args[0])

    def test_deny_any_real_request(self):
        with patch('bx_py_utils.test_utils.deny_requests.DenyAnyRealRequestContextManager.__enter__') as mock:
            deny_any_real_request()
        mock.assert_called_once()
