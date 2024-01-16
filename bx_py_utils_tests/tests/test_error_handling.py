from unittest import TestCase

from bx_py_utils.error_handling import print_exc_plus
from bx_py_utils.test_utils.redirect import RedirectOut


class ErrorHandlingTestCase(TestCase):
    def test_print_exc_plus(self):
        test_message = 'Only a Test'

        with RedirectOut() as buffer:
            try:
                raise AssertionError(test_message)
            except BaseException:  # noqa: B036
                print_exc_plus()

            self.assertEqual(buffer.stdout, '')
            output = buffer.stderr
            self.assertIn('Locals by frame, most recent call first:', output)
            self.assertIn('/bx_py_utils_tests/tests/test_error_handling.py", line', output)
            self.assertIn("test_message = 'Only a Test'", output)

    def test_print_exc_plus_max_chars(self):
        with RedirectOut() as buffer:
            try:
                x = '12345678901234567890'
                raise AssertionError(x)
            except BaseException:  # noqa: B036
                print_exc_plus(max_chars=15)

            self.assertEqual(buffer.stdout, '')
            output = buffer.stderr
            self.assertIn('Locals by frame, most recent call first:', output)
            self.assertIn('/bx_py_utils_tests/tests/test_error_handling.py", line', output)
            self.assertIn("x = '12345678901...", output)
