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


def write_json_file(path: Path | str, data: dict, **json_kwargs):
    path = Path(path)

    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=f'{path.name}.', suffix='.tmp', mode='w', encoding='utf-8', delete=False
    ) as tmp_handle:
        tmp_path = Path(tmp_handle.name)
        try:
            json.dump(data, tmp_handle, **json_kwargs)
            tmp_handle.flush()

            tmp_path.rename(path)
        except BaseException:
            # Necessary for Python <3.12, where NamedTemporaryFile crashes if the file is no longer present
            tmp_path.unlink(missing_ok=True)
            raise


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
