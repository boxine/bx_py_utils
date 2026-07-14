from unittest import TestCase

from bx_py_utils.list_utils import unique_list


class ListUtilsTestCase(TestCase):
    def test_unique_list(self):
        self.assertEqual(unique_list([5, 1, 2, 5, 3, 2, 5, 4]), [5, 1, 2, 3, 4])
