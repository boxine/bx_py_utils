import inspect
import sys
from unittest import TestCase

from bx_py_utils.test_utils.redirect import RedirectOut


class RedirectTestCase(TestCase):
    def test_happy_path(self):
        with RedirectOut() as buffer:
            print('out')
            print('err', file=sys.stderr)

        self.assertEqual(buffer.stdout, 'out\n')
        self.assertEqual(buffer.stderr, 'err\n')

        with RedirectOut(strip=True) as buffer:
            print('\n out ')
            print('\n err ', file=sys.stderr)

        self.assertEqual(buffer.stdout, 'out')
        self.assertEqual(buffer.stderr, 'err')

    def test_only_stdout(self):
        with RedirectOut() as buffer:
            print('out')

        self.assertEqual(buffer.stdout, 'out\n')
        self.assertEqual(buffer.stderr, '')

    def test_only_stderr(self):
        with RedirectOut() as buffer:
            print('err', file=sys.stderr)

        self.assertEqual(buffer.stdout, '')
        self.assertEqual(buffer.stderr, 'err\n')

    def test_no_output(self):
        with RedirectOut() as buffer:
            pass
        self.assertEqual(buffer.stdout, '')
        self.assertEqual(buffer.stderr, '')

    def test_print_fallback_on_error(self):
        with RedirectOut(strip=True) as buffer1, self.assertRaises(ValueError) as cm:
            with RedirectOut() as buffer2:
                print('out')
                print('err', file=sys.stderr)
                raise ValueError('A test error!')

        # The inner buffer should capture the output as usual until the exception:
        self.assertEqual(buffer2.stdout, 'out\n')
        self.assertEqual(buffer2.stderr, 'err\n')

        # Check that the RedirectOut() will print the captured output + error when an exception is raised:
        self.assertEqual(buffer1.stdout, '')
        self.assertEqual(
            buffer1.stderr.strip(),
            inspect.cleandoc("""
                Exception raised while buffer ValueError: A test error!
                ∨∨∨∨∨∨∨∨∨∨∨∨ [captured stdout+err] ∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨
                out
                err
                ∧∧∧∧∧∧∧∧∧∧∧∧ [captured stdout+err] ∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧
            """),
        )
        self.assertEqual(str(cm.exception), 'A test error!')
