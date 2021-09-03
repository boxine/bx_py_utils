from pathlib import Path

import pytest

from bx_py_utils.path import assert_is_dir, assert_is_file, read_json_file


def test_assert_is_dir():
    with pytest.raises(NotADirectoryError) as cm:
        assert_is_dir(path='/foo/bar')
    assert str(cm.value) == 'Directory does not exists: "/foo/bar"'

    self_path = Path(__file__).parent
    assert_is_dir(path=self_path)
    assert_is_dir(path=str(self_path))


def test_assert_is_file():
    with pytest.raises(NotADirectoryError) as cm:
        assert_is_file(path='/foo/bar.txt')
    assert str(cm.value) == 'Directory does not exists: "/foo"'

    self_file_path = Path(__file__)

    not_existing_file_path = self_file_path.parent / 'foobar.txt'
    with pytest.raises(FileNotFoundError) as cm:
        assert_is_file(path=not_existing_file_path)
    assert str(cm.value) == f'File does not exists: "{not_existing_file_path}"'

    assert_is_file(path=self_file_path)
    assert_is_file(path=str(self_file_path))


def test_read_json_file():
    json_path = Path(__file__).parent / 'json_file.json'
    data = read_json_file(json_path)
    assert data == {
        'foo': ['bar', 42],
    }
