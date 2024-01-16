import datetime
import pathlib
import re
import tempfile
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch
from uuid import UUID

import typeguard

import bx_py_utils
from bx_py_utils import html_utils
from bx_py_utils.environ import OverrideEnviron
from bx_py_utils.html_utils import ElementsNotFoundError
from bx_py_utils.test_utils import snapshot
from bx_py_utils.test_utils.assertion import pformat_ndiff, text_ndiff
from bx_py_utils.test_utils.datetime import parse_dt
from bx_py_utils.test_utils.filesystem_utils import FileWatcher
from bx_py_utils.test_utils.snapshot import (
    _AUTO_SNAPSHOT_NAME_COUNTER,
    _get_caller_names,
    assert_binary_snapshot,
    assert_html_snapshot,
    assert_py_snapshot,
    assert_snapshot,
    assert_text_snapshot,
    get_snapshot_file,
)


SELF_PATH = pathlib.Path(__file__).parent


class SnapshotTestCase(TestCase):
    def test_get_snapshot_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            snapshot_file = get_snapshot_file(root_dir=tmp_dir, snapshot_name='foo_bar', extension='.123')
            assert snapshot_file == pathlib.Path(tmp_dir) / 'foo_bar.snapshot.123'
            assert not snapshot_file.is_file()

            snapshot_file = get_snapshot_file(root_dir=tmp_dir, snapshot_name='foobar.snapshot', extension='.txt')
            assert snapshot_file == pathlib.Path(tmp_dir) / 'foobar.snapshot.txt'
            assert not snapshot_file.is_file()

    def test_assert_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(FileNotFoundError) as cm:
                assert_snapshot(tmp_dir, 'snap', [{'foo': 42, 'bär': 5}])
            error_message = str(cm.exception)
            self.assertIn('No such file or directory', error_message)
            self.assertIn(tmp_dir, error_message)
            self.assertIn('snap.snapshot.json', error_message)

            assert_snapshot(tmp_dir, 'snap', [{'foo': 42, 'bär': 5}])

            # ndiff error message:

            with self.assertRaises(AssertionError) as exc_info:
                assert_snapshot(tmp_dir, 'snap', [{'foo': 42, 'bär': 23}], diff_func=pformat_ndiff)
            self.assertEqual(
                str(exc_info.exception),
                'snap\n'
                '  [\n'
                '      {\n'
                '-         "bär": 23,\n'
                '?                ^^\n'
                '\n'
                '+         "bär": 5,\n'
                '?                ^\n'
                '\n'
                '          "foo": 42\n'
                '      }\n'
                '  ]',
            )

            # unified diff error message:

            with self.assertRaises(AssertionError) as exc_info:
                assert_snapshot(tmp_dir, 'snap', [{'foo': 42, 'bär': 123}])
            self.assertEqual(
                str(exc_info.exception),
                'snap\n'
                '--- got\n'
                '\n'
                '+++ expected\n'
                '\n'
                '@@ -1,6 +1,6 @@\n'
                '\n'
                ' [\n'
                '     {\n'
                '-        "bär": 123,\n'
                '+        "bär": 23,\n'
                '         "foo": 42\n'
                '     }\n'
                ' ]',
            )

            # invalid type
            with self.assertRaises(AssertionError) as exc_info, typeguard.suppress_type_checks():
                assert_snapshot(
                    tmp_dir,
                    'invalid_type',
                    got={1, 2},  # noqa - set() is not allowed!
                )
            self.assertEqual(
                str(exc_info.exception),
                'Not JSON-serializable: {1, 2} is not a dict or list, but a set',
            )

        # Specify a name suffix:
        with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'), tempfile.TemporaryDirectory() as tmp_dir:
            assert_snapshot(tmp_dir, got=[1, 2, 3], name_suffix='suffix')
            self.assertEqual(
                [item.name for item in pathlib.Path(tmp_dir).iterdir()],
                ['test_test_utils_snapshot_assert_snapshot_suffix_1.snapshot.json'],
            )

    def test_assert_snapshot_with_tuple(self):
        """
        assert_snapshot() should not been used, if objects contains tuple()
        Test that the diff indicates the problem.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(FileNotFoundError) as cm:
                assert_snapshot(tmp_dir, 'snap', [('foo', 42), 1, 1.5])
            assert 'snap.snapshot.json' in str(cm.exception)

            written_json = (pathlib.Path(tmp_dir) / 'snap.snapshot.json').read_text()
            written_json = re.sub(r'\s+', '', written_json)
            # The tuple() are "converted" to lists:
            assert written_json == '[["foo",42],1,1.5]'

            # tuple() doesn't work with assert_snapshot(self):
            with self.assertRaises(AssertionError) as exc_info:
                assert_snapshot(tmp_dir, 'snap', [('foo', 42), 1, 1.5])
            self.assertEqual(
                str(exc_info.exception),
                'snap\n'
                '--- got\n\n'
                '+++ expected\n\n'
                '@@ -1 +1 @@\n\n'
                "-[('foo', 42), 1, 1.5]\n"
                "+[['foo', 42], 1, 1.5]",
            )

    def test_assert_text_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            TEXT = 'this is\nmultiline "text"\none\ntwo\nthree\nfour'
            with self.assertRaises(FileNotFoundError):
                assert_text_snapshot(tmp_dir, 'text', TEXT)
            written_text = (pathlib.Path(tmp_dir) / 'text.snapshot.txt').read_text()
            assert written_text == TEXT

            assert_text_snapshot(tmp_dir, 'text', TEXT)

            # Error message with ndiff:

            with self.assertRaises(AssertionError) as exc_info:
                assert_text_snapshot(
                    tmp_dir,
                    'text',
                    'this is:\nmultiline "text"\none\ntwo\nthree\nfour',
                    diff_func=text_ndiff,
                )
            written_text = (pathlib.Path(tmp_dir) / 'text.snapshot.txt').read_text()
            assert written_text == 'this is:\nmultiline "text"\none\ntwo\nthree\nfour'
            self.assertEqual(
                str(exc_info.exception),
                'text\n'
                '- this is:\n'
                '?        -\n'
                '\n'
                '+ this is\n'
                '  multiline "text"\n'
                '  one\n'
                '  two\n'
                '  three\n'
                '  four',
            )

            # Error message with unified diff:

            with self.assertRaises(AssertionError) as exc_info:
                assert_text_snapshot(
                    tmp_dir,
                    'text',
                    'This is:\nmultiline "text"\none\ntwo\nthree\nfour',
                )
            self.assertEqual(
                str(exc_info.exception),
                'text\n'
                '--- got\n'
                '\n'
                '+++ expected\n'
                '\n'
                '@@ -1,4 +1,4 @@\n'
                '\n'
                '-This is:\n'
                '+this is:\n'
                ' multiline "text"\n'
                ' one\n'
                ' two',
            )

            assert_text_snapshot(tmp_dir, 'text', 'This is:\nmultiline "text"\none\ntwo\nthree\nfour')

            with self.assertRaises(FileNotFoundError):
                assert_text_snapshot(tmp_dir, 'text', TEXT, extension='.test2')
            written_text = (pathlib.Path(tmp_dir) / 'text.snapshot.test2').read_text()
            assert written_text == TEXT

            # Newlines
            UNIX_TEXT = 'a\nnewline'
            WINDOWS_TEXT = 'a\r\nnewline'
            with self.assertRaises(FileNotFoundError):
                assert_text_snapshot(tmp_dir, 'newlines', UNIX_TEXT)
            written_bytes = (pathlib.Path(tmp_dir) / 'newlines.snapshot.txt').read_bytes()
            assert written_bytes == UNIX_TEXT.encode('utf-8')

            with self.assertRaises(AssertionError) as exc_info:
                assert_text_snapshot(tmp_dir, 'newlines', WINDOWS_TEXT)
            written_bytes = (pathlib.Path(tmp_dir) / 'newlines.snapshot.txt').read_bytes()
            assert written_bytes == WINDOWS_TEXT.encode('utf-8')
            self.assertEqual(
                str(exc_info.exception),
                '''Differing newlines: Expected 'a\\nnewline', got 'a\\r\\nnewline\'''',
            )

            with self.assertRaises(AssertionError) as cm:
                assert_text_snapshot(tmp_dir, snapshot_name='type_error', got=None)
            self.assertEqual(
                cm.exception.args,
                ('Got None of type NoneType, but expected a str',),
            )

        # Specify a name suffix:
        with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'), tempfile.TemporaryDirectory() as tmp_dir:
            assert_text_snapshot(tmp_dir, got='foo', name_suffix='suffix')
            self.assertEqual(
                [item.name for item in pathlib.Path(tmp_dir).iterdir()],
                ['test_test_utils_snapshot_assert_text_snapshot_suffix_1.snapshot.txt'],
            )

    def test_assert_py_snapshot(self):
        example = {
            'uuid': UUID('00000000-0000-0000-1111-000000000001'),
            'datetime': parse_dt('2020-01-01T00:00:00+0000'),
            'date': datetime.date(2000, 1, 2),
            'time': datetime.time(3, 4, 5),
            'decimal': Decimal('3.14'),
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(FileNotFoundError):
                assert_py_snapshot(tmp_dir, 'snap', example)

            assert_py_snapshot(tmp_dir, 'snap', example)

            example['uuid'] = '00000000-0000-0000-1111-000000000001'
            with self.assertRaises(AssertionError) as exc_info:
                assert_py_snapshot(tmp_dir, 'snap', example)
            self.assertEqual(
                str(exc_info.exception),
                "snap\n"
                "--- got\n"
                "\n"
                "+++ expected\n"
                "\n"
                "@@ -2,4 +2,4 @@\n"
                "\n"
                "     'datetime': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),\n"
                "     'decimal': Decimal('3.14'),\n"
                "     'time': datetime.time(3, 4, 5),\n"
                "-    'uuid': '00000000-0000-0000-1111-000000000001'}\n"
                "+    'uuid': UUID('00000000-0000-0000-1111-000000000001')}",
            )

        # Specify a name suffix:
        with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'), tempfile.TemporaryDirectory() as tmp_dir:
            assert_py_snapshot(tmp_dir, got={1: 2}, name_suffix='suffix')
            self.assertEqual(
                [item.name for item in pathlib.Path(tmp_dir).iterdir()],
                ['test_test_utils_snapshot_assert_py_snapshot_suffix_1.snapshot.txt'],
            )

    def test_assert_binary_snapshot(self):
        expected = b'\xAB\x00'
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(FileNotFoundError):
                assert_binary_snapshot(tmp_dir, 'binary-snap', expected)

            assert_binary_snapshot(tmp_dir, 'binary-snap', expected)

            got = b'\xAB\xFF\x00\xCC'
            with self.assertRaises(AssertionError) as exc_info:
                assert_binary_snapshot(tmp_dir, 'binary-snap', got)
            self.assertEqual(
                str(exc_info.exception),
                'binary-snap\n'
                'expected: 2 Bytes, MD5 45aa1f1c9622b4a0f817b177a1b84f78\n'
                'got: 4 Bytes, MD5 02df4e34a310564c0bb6245c432eb15e',
            )

        # Specify a name suffix:
        with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'), tempfile.TemporaryDirectory() as tmp_dir:
            assert_binary_snapshot(tmp_dir, got=b'foo', name_suffix='suffix')
            self.assertEqual(
                [item.name for item in pathlib.Path(tmp_dir).iterdir()],
                ['test_test_utils_snapshot_assert_binary_snapshot_suffix_1.snapshot.bin'],
            )

    def test_auto_source_names(self):
        root_dir, snapshot_name = _get_caller_names()
        assert root_dir == SELF_PATH

        # Name of this file + name of this test function + sequential number
        assert snapshot_name == 'test_test_utils_snapshot_auto_source_names_1.snapshot'

        # Call it again -> sequential number =+ 1 ???

        root_dir, snapshot_name = _get_caller_names()
        assert root_dir == SELF_PATH
        assert snapshot_name == 'test_test_utils_snapshot_auto_source_names_2.snapshot'

        # set own root_dir
        own_root_dir = pathlib.Path(bx_py_utils.__file__).parent
        root_dir, snapshot_name = _get_caller_names(root_dir=own_root_dir)
        assert root_dir == own_root_dir
        assert snapshot_name == 'test_test_utils_snapshot_auto_source_names_1.snapshot'

        # Set not existing root_dir:
        with self.assertRaises(NotADirectoryError) as cm:
            _get_caller_names(root_dir='/foo/bar')
        self.assertEqual(
            cm.exception.args,
            ('Directory does not exists: "/foo/bar"',),
        )

        # set own snapshot name
        root_dir, snapshot_name = _get_caller_names(snapshot_name='foo_bar')
        self.assertEqual(root_dir, SELF_PATH)
        self.assertEqual(snapshot_name, 'foo_bar')

        # not valid snapshot name
        with self.assertRaises(AssertionError) as cm:
            _get_caller_names(snapshot_name='Foo Bar!')
        self.assertEqual(
            cm.exception.args,
            ("Invalid snapshot name: 'Foo Bar!'",),
        )

        # Add a name suffix:
        root_dir, snapshot_name = _get_caller_names(name_suffix='django42')
        self.assertEqual(root_dir, SELF_PATH)
        self.assertEqual(snapshot_name, 'test_test_utils_snapshot_auto_source_names_django42_1.snapshot')

        # own name + suffix:
        with self.assertRaises(AssertionError) as cm:
            _get_caller_names(snapshot_name='foo', name_suffix='bar')
        self.assertEqual(
            cm.exception.args,
            ("Specify only name or suffix, not both: snapshot_name='foo' name_suffix='bar'",),
        )

        # not valid suffix:
        with self.assertRaises(AssertionError) as cm:
            _get_caller_names(name_suffix='Foo Bar!')
        self.assertEqual(
            cm.exception.args,
            ("Invalid name suffix: 'Foo Bar!'",),
        )

    def test_assert_py_snapshot_auto_names(self):
        snapshot_filename1 = 'test_test_utils_snapshot_assert_py_snapshot_auto_names_1.snapshot.txt'
        snapshot_filename2 = 'test_test_utils_snapshot_assert_py_snapshot_auto_names_2.snapshot.txt'
        snapshot_path1 = SELF_PATH / snapshot_filename1
        snapshot_path2 = SELF_PATH / snapshot_filename2

        example = [1, 2, 3]

        with FileWatcher(base_path=SELF_PATH, cleanup=True) as file_watcher:
            with self.assertRaises(FileNotFoundError):
                assert_py_snapshot(got=example)

            assert snapshot_path1.is_file()

            # Check created files: Is that only our expected files?
            new_files = file_watcher.get_new_items()
            assert new_files == {snapshot_path1}

            # We would like to check the same file ;)
            _AUTO_SNAPSHOT_NAME_COUNTER.clear()

            assert_py_snapshot(got=example)

            # Will a second test file created?

            with self.assertRaises(FileNotFoundError):
                assert_py_snapshot(got=example)

            assert snapshot_path1.is_file()
            assert snapshot_path2.is_file()

            # Check created files: Is that only our expected files?
            new_files = file_watcher.get_new_items()
            assert new_files == {snapshot_path1, snapshot_path2}

    def test_assert_text_snapshot_auto_names(self):
        snapshot_path = SELF_PATH / ('test_test_utils_snapshot_assert_text_snapshot_auto_names_1.snapshot.txt')
        example = 'Foo Bar!'
        with FileWatcher(base_path=SELF_PATH, cleanup=True) as file_watcher:
            with self.assertRaises(FileNotFoundError):
                assert_text_snapshot(got=example)

            # Check created files: Is that only our expected files?
            new_files = file_watcher.get_new_items()
            assert new_files == {snapshot_path}

            # We would like to check the same file ;)
            _AUTO_SNAPSHOT_NAME_COUNTER.clear()

            assert_text_snapshot(got=example)

            # We would like to check the same file ;)
            _AUTO_SNAPSHOT_NAME_COUNTER.clear()

            # We can specify the path used to get the caller stack frame:
            assert_text_snapshot(got=example, self_file_path=pathlib.Path(snapshot.__file__))

    def test_assert_html_snapshot(self):
        html = '''
            <!DOCTYPE html> \r\n <html> \r\n  \r\n <head>
             \r\n  \r\n <title \r\n >Page Title</title></head> \r\n  \r\n <body>
            <h1>This is a Heading</h1> \r\n  \r\n
            <p \r\n >This is a paragraph.</p> \r\n  \r\n
            </body> \r\n  \r\n </html>
        '''
        assert_html_snapshot(got=html)

        # Specify a name suffix:
        with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'), tempfile.TemporaryDirectory() as tmp_dir:
            assert_html_snapshot(tmp_dir, got='<foo />', name_suffix='suffix')
            self.assertEqual(
                [item.name for item in pathlib.Path(tmp_dir).iterdir()],
                ['test_test_utils_snapshot_assert_html_snapshot_suffix_1.snapshot.html'],
            )

    def test_assert_html_snapshot_without_lxml(self):
        with patch.object(html_utils, 'html', None), self.assertRaises(ModuleNotFoundError) as cm:
            assert_html_snapshot(got='')

        self.assertEqual(
            cm.exception.args,
            ('This feature needs "lxml", please add it to you requirements',),
        )

    def test_assert_html_snapshot_by_css_selector(self):
        html = '''
            <!DOCTYPE html> \r\n <html> \r\n  \r\n <head>
             \r\n  \r\n <title \r\n >Page Title</title></head> \r\n  \r\n <body>
            <h1>This is a Heading</h1> \r\n  \r\n
            <p \r\n >This is a paragraph.</p> \r\n  \r\n
            <div class="test-me"><b>some Content 1</b></div>
            <div class="test-me"><i>some Content 2</i></div>
            </body> \r\n  \r\n </html>
        '''
        assert_html_snapshot(got=html, query_selector='div.test-me')

        try:
            assert_html_snapshot(got=html, query_selector='div.not-found')
            raise AssertionError('Expected ElementsNotFoundError, no Error was raised')
        except ElementsNotFoundError:
            pass
        except Exception as err:
            raise AssertionError('Expected ElementsNotFoundError, other Error was raised: ', err)

    def test_raise_snapshot_errors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = pathlib.Path(temp_dir)
            snapshot_path = temp_path / 'snap.snapshot.json'
            self.assertFalse(snapshot_path.exists())

            with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'):
                assert_snapshot(root_dir=temp_path, snapshot_name='snap', got=[])
            self.assertTrue(snapshot_path.is_file())
            snapshot_path.unlink()

            with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='1'), self.assertRaises(FileNotFoundError) as exc_info:
                assert_snapshot(root_dir=temp_path, snapshot_name='snap', got=[])
            self.assertIn('No such file or directory', str(exc_info.exception))
