import os
from unittest import TestCase
from unittest.mock import mock_open, patch

from bx_py_utils.environ import OverrideEnviron, cgroup_memory_usage


class DockerTestCase(TestCase):
    def test_cgroup_memory_usage(self):
        expectations = {
            'B': 524288000,
            'KB': 524288000 / 1024,
            'MB': 524288000 / 1024 ** 2,
            'GB': 524288000 / 1024 ** 3,
            'TB': 524288000 / 1024 ** 4,
        }

        for unit, value in expectations.items():
            with patch('bx_py_utils.environ.open', mock_open(read_data='524288000')) as m:
                usage = cgroup_memory_usage(unit=unit)
            m.assert_called_once_with('/sys/fs/cgroup/memory/memory.usage_in_bytes', 'r')
            assert usage == value


class OverrideEnvironTestCase(TestCase):
    def test_basic(self):
        old_value = os.environ.get('LOGNAME')

        with OverrideEnviron(LOGNAME='foo'):
            self.assertEqual(os.environ['LOGNAME'], 'foo')

            with OverrideEnviron(LOGNAME='bar'):
                self.assertEqual(os.environ['LOGNAME'], 'bar')

                with OverrideEnviron(LOGNAME=None, FOO='bar'):
                    self.assertNotIn('LOGNAME', os.environ)
                    self.assertEqual(os.environ['FOO'], 'bar')

                self.assertNotIn('FOO', os.environ)
                self.assertEqual(os.environ['LOGNAME'], 'bar')
            self.assertEqual(os.environ['LOGNAME'], 'foo')

        self.assertEqual(os.environ.get('LOGNAME'), old_value)
