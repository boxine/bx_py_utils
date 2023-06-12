import json
import os
import tempfile
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


class ChangeCurrentWorkDir:
    """
    Context Manager change the "CWD" to an other directory.
    """

    def __init__(self, path):
        self.path = path
        self.old_cwd = Path().cwd()

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)
        if exc_type:
            return False


class MockCurrentWorkDir(tempfile.TemporaryDirectory):
    """
    Context Manager to move the "CWD" to a temp directory.
    """

    def __init__(self, **kwargs):
        self.old_cwd = Path().cwd()
        super().__init__(**kwargs)

    def __enter__(self):
        temp_dir = super().__enter__()
        os.chdir(temp_dir)
        self.temp_path = Path(temp_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        os.chdir(self.old_cwd)
        if exc_type:
            return False
