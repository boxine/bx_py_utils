import json
from pathlib import Path


def assert_is_dir(path):
    """
    Check if given path is a directory
    """
    if not isinstance(path, Path):
        path = Path(path)

    if not path.is_dir():
        raise NotADirectoryError(f'Directory does not exists: "{path}"')


def assert_is_file(path):
    """
    Check if given path is a file
    """
    if not isinstance(path, Path):
        path = Path(path)

    assert_is_dir(path.parent)

    if not path.is_file():
        raise FileNotFoundError(f'File does not exists: "{path}"')


def read_json_file(path):
    if not isinstance(path, Path):
        path = Path(path)

    with path.open('rb') as f:
        return json.load(f)
