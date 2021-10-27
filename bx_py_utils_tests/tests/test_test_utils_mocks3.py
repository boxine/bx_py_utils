import time
from unittest import mock

from bx_py_utils.test_utils.mocks3 import PseudoS3Client
from bx_py_utils.test_utils.snapshot import assert_text_snapshot


def test_debug_long_repr():
    s3 = PseudoS3Client(init_buckets=('b-bucket', 'a-bucket'))
    s3.mock_set_content('a-bucket', 'a-key', b'<?xml?><a complicated="document">')
    s3.mock_set_content('a-bucket', 'empty', b'')
    s3.mock_set_content('a-bucket', 'binary', b'\xf0\x00' * 42)
    s3.mock_set_content('a-bucket', 'png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\xb0')
    s3.mock_set_content('a-bucket', 'short', b'short')
    s3.mock_set_content('a-bucket', 'short-binary', b's\x00\xf0hort')
    s3.mock_set_content('b-bucket', 'very-long-key-that-is-way-too-long', b'but short content')

    got = s3.debug_long_repr()
    assert_text_snapshot(got=got)
