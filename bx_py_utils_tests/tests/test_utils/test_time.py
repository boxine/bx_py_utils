import time
from unittest import TestCase, mock

from bx_py_utils.test_utils.time import MockTimeMonotonicGenerator


class TimeTestUtilsTestCase(TestCase):
    def test_time_monotonic_mock(self):
        with mock.patch.object(time, 'monotonic', MockTimeMonotonicGenerator()):
            now = time.monotonic()
            self.assertIsInstance(now, float)
            self.assertEqual(now, 1.0)
            self.assertEqual(time.monotonic(), 2.0)
            self.assertEqual(time.monotonic(), 3.0)

        with mock.patch.object(time, 'monotonic', MockTimeMonotonicGenerator(offset=10)):
            now = time.monotonic()
            self.assertIsInstance(now, float)
            self.assertEqual(now, 10.0)
            self.assertEqual(time.monotonic(), 20.0)
            self.assertEqual(time.monotonic(), 30.0)

        with mock.patch.object(time, 'monotonic_ns', MockTimeMonotonicGenerator(offset=100, cast_func=int)):
            now = time.monotonic_ns()
            self.assertIsInstance(now, int)
            self.assertEqual(now, 100)
            self.assertEqual(time.monotonic_ns(), 200)
            self.assertEqual(time.monotonic_ns(), 300)
