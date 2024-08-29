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
