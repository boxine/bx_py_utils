import unittest
from unittest.mock import patch

from bx_py_utils.test_utils.context_managers import MassContextManager
from bx_py_utils_tests.tests import mass_context_manager_test_helper
from bx_py_utils_tests.tests.mass_context_manager_test_helper import get_foo_bar


class FooBarMocks(MassContextManager):
    mocks = (
        patch.object(mass_context_manager_test_helper, 'foo', return_value='Mocked-FOO'),
        patch.object(mass_context_manager_test_helper, 'bar', return_value='Mocked-BAR'),
    )


class TestMassContextManager(unittest.TestCase):

    def test_as_context_manager(self):
        self.assertEqual(get_foo_bar(), 'foo bar')

        with FooBarMocks() as cm:
            self.assertEqual(get_foo_bar(), 'Mocked-FOO Mocked-BAR')

        self.assertEqual(len(cm.patchers), 2)
        for patcher in cm.patchers:
            patcher.assert_called_once_with()

        self.assertEqual(get_foo_bar(), 'foo bar')

    def test_as_decorator(self):
        def undecroated():
            return get_foo_bar()

        @FooBarMocks()
        def decorated():
            return get_foo_bar()

        self.assertEqual(undecroated(), 'foo bar')
        self.assertEqual(decorated(), 'Mocked-FOO Mocked-BAR')
