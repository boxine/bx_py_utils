import logging
from unittest import TestCase

from bx_py_utils.test_utils.log_utils import NoLogs, RaiseLogUsage


class LogHandlerTestCase(TestCase):
    def test_raise_log_usage(self):
        with self.assertRaises(AssertionError) as cm:
            logger = logging.getLogger('test_raise_log_usage')
            logger.handlers = [RaiseLogUsage()]
            logger.warning('foobar')

        assert cm.exception.args[0].startswith('Missing log capture')

    def test_no_logs(self):
        logger = logging.getLogger('foobar')

        with self.assertLogs('foobar') as logs:
            logger.info('Before')

            with NoLogs(logger_name='foobar'):
                logger.info('Message to Nirvana')

            logger.info('After')

        self.assertEqual(logs.output, ['INFO:foobar:Before', 'INFO:foobar:After'])
