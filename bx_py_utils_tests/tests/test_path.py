from pathlib import Path
from unittest import TestCase

from bx_py_utils.path import assert_is_dir, assert_is_file, read_json_file, write_json_file


class PathTestCase(TestCase):
    def test_assert_is_dir(self):
        with self.assertRaises(NotADirectoryError) as cm:
            assert_is_dir(path='/foo/bar')
        self.assertEqual(
            cm.exception.args,
            ('Directory does not exists: "/foo/bar"',),
        )

        self_path = Path(__file__).parent
        assert_is_dir(path=self_path)
        assert_is_dir(path=str(self_path))

    def test_assert_is_file(self):
        with self.assertRaises(NotADirectoryError) as cm:
            assert_is_file(path='/foo/bar.txt')
        self.assertEqual(
            cm.exception.args,
            ('Directory does not exists: "/foo"',),
        )

        self_file_path = Path(__file__)

        not_existing_file_path = self_file_path.parent / 'foobar.txt'
        with self.assertRaises(FileNotFoundError) as cm:
            assert_is_file(path=not_existing_file_path)
        self.assertEqual(
            cm.exception.args,
            (f'File does not exists: "{not_existing_file_path}"',),
        )

        assert_is_file(path=self_file_path)
        assert_is_file(path=str(self_file_path))

    def test_read_json_file(self):
        json_path = Path(__file__).parent / 'json_file.json'
        data = read_json_file(json_path)
        assert data == {
            'foo': ['bar', 42],
        }

    def test_write_json_file(self):
        obj = {
            'foo': ['bär', 42],
        }
        json_path = Path(__file__).parent / 'write_json_file.json'
        write_json_file(json_path, obj, ensure_ascii=False)
        text = json_path.read_text()
        self.assertEqual(text, '{"foo": ["bär", 42]}')

        broken_json_path = Path(__file__).parent / 'write_json_file_broken.json'
        with self.assertRaises(TypeError):
            write_json_file(json_path, {object(): 'not JSON'}, ensure_ascii=False)
        assert not broken_json_path.exists()
