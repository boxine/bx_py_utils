import io
import pathlib
import re
import tempfile
from unittest import TestCase

from bx_py_utils.test_utils.mocks3 import PseudoS3Client
from bx_py_utils.test_utils.snapshot import assert_snapshot, assert_text_snapshot


class CountingCallback:
    def __init__(self):
        self.total_bytes = 0

    def __call__(self, byte_count):
        self.total_bytes += byte_count


class S3MockTest(TestCase):
    def test_debug_long_repr(self):
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

    def test_various_get_file(self):
        s3 = PseudoS3Client(init_buckets=('buck',))
        content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\xb0'
        s3.mock_set_content('buck', 'png', content)

        # download_file
        with tempfile.TemporaryDirectory() as tmp_dir:
            existing_path = pathlib.Path(tmp_dir) / 'existing'
            callback = CountingCallback()
            s3.download_file('buck', 'png', str(existing_path), Callback=callback)
            self.assertEqual(callback.total_bytes, len(content))
            self.assertEqual(existing_path.read_bytes(), content)

            not_found_path = pathlib.Path(tmp_dir) / 'not-found'
            with self.assertRaises(s3.exceptions.NoSuchKey):
                s3.download_file('buck', 'png404', str(not_found_path))
            assert not not_found_path.exists()

        # download_fileobj
        callback = CountingCallback()
        buf = io.BytesIO()
        s3.download_fileobj(Bucket='buck', Key='png', Fileobj=buf, Callback=callback)
        self.assertEqual(buf.getvalue(), content)
        self.assertEqual(callback.total_bytes, len(content))

        not_found_buf = io.BytesIO()
        with self.assertRaises(s3.exceptions.NoSuchKey):
            s3.download_file('buck', 'png404', not_found_buf)
        self.assertEqual(not_found_buf.getvalue(), b'')

        # get_file
        got = s3.get_object(Bucket='buck', Key='png')
        self.assertEqual(got['Body'].read(), content)
        self.assertEqual(got['ContentLength'], len(content))

        with self.assertRaises(s3.exceptions.NoSuchKey):
            s3.get_object(Bucket='buck', Key='png404')

        # Mock
        self.assertEqual(s3.mock_get_content('buck', 'png'), content)

    def test_list_bucket(self):
        s3 = PseudoS3Client(init_buckets=('buck',))
        s3.mock_set_content('buck', 'foo/bar/baz', b'123')
        s3.mock_set_content('buck', 'xxx', b'456')
        s3.mock_set_content('buck', 'foo/zzz', b'last.')
        s3.mock_set_content('buck', 'foo/aaa', b'first!')

        paginator = s3.get_paginator('list_objects_v2')

        # List without prefix
        res = []
        for page in paginator.paginate(Bucket='buck'):
            res.extend(page['Contents'])
        assert_snapshot(got=res)

        # List with prefix
        res = []
        for page in paginator.paginate(Bucket='buck', Prefix='foo/'):
            res.extend(page['Contents'])
        assert_snapshot(got=res)

        # Mock function
        self.assertEqual(s3.mock_list_files('buck'), ['foo/aaa', 'foo/bar/baz', 'foo/zzz', 'xxx'])

    def test_list_buckets(self):
        s3 = PseudoS3Client(init_buckets=('buck', 'foo-bar-123'))
        bucket_names = set(b['Name'] for b in s3.list_buckets()['Buckets'])
        self.assertEqual(bucket_names, {'buck', 'foo-bar-123'})
        self.assertEqual(s3.head_bucket('buck')['ResponseMetadata']['HTTPStatusCode'], 200)

        with self.assertRaises(s3.exceptions.NoSuchKey):
            s3.head_bucket('hole-in-bucket')

    def test_upload_fileobj_closed_file(self):
        s3 = PseudoS3Client(init_buckets=('foo',))
        with tempfile.TemporaryFile() as temp_file:
            assert not temp_file.closed
            s3.upload_fileobj(Fileobj=temp_file, Bucket='foo', Key='bar')
            assert temp_file.closed

    def test_head_object(self):
        s3 = PseudoS3Client(init_buckets=('a-bucket',))
        s3.mock_set_content('a-bucket', 'a-key', b'foobar')

        res = s3.head_object('a-bucket', 'a-key')
        self.assertEqual(res['ContentLength'], 6)

        expected_message = (
            'An error occurred (404) when calling the HeadObject operation: Not Found')
        with self.assertRaisesRegex(s3.exceptions.ClientError, re.escape(expected_message)):
            s3.head_object('a-bucket', 'no-such-key')

        with self.assertRaisesRegex(s3.exceptions.ClientError, re.escape(expected_message)):
            s3.head_object('b-bucket', 'no-such-bucket')
