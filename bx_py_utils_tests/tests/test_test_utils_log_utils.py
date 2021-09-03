import logging
from unittest import TestCase

from bx_py_utils.test_utils.log_utils import RaiseLogUsage


class LogHandlerTestCase(TestCase):
    def test_raise_log_usage(self):
        with self.assertRaises(AssertionError) as cm:
            logger = logging.getLogger('test_raise_log_usage')
            logger.handlers = [RaiseLogUsage()]
            logger.warning('foobar')

        assert cm.exception.args[0].startswith('Missing log capture')
