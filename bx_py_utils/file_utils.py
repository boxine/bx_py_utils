import io
import tempfile
from pathlib import Path
from typing import BinaryIO


class EmptyFileError(AssertionError):
    """
    Will be raised from get_and_assert_file_size() if a 0-bytes file was found.
    """
    pass


def get_and_assert_file_size(file_object: BinaryIO, msg: str) -> int:
    """
    Check file size of given file object. Raise EmptyFileError for empty files or return size
    """
    file_object.seek(0, io.SEEK_END)  # go to end of the file
    file_size = file_object.tell()
    file_object.seek(0)
    if not file_size:
        raise EmptyFileError(f'Empty file error: {msg}')
    return file_size


class NamedTemporaryFile2(tempfile.TemporaryDirectory):
    """
    Generates a temp file with the given filename **without** any random name sequence.

    Note: Normal NamedTemporaryFile will get a random name sequence to get a unique name!
    This is here not the case! Because we always store the file into a temp directory!
    """

    def __init__(self, file_name: str, mode='w+b', buffering=-1):
        self.file_name = file_name
        assert self.file_name
        self.mode = mode
        self.buffering = buffering
        super().__init__()

    def __enter__(self):
        temp_dir_name = Path(super().__enter__())
        temp_path = Path(temp_dir_name / self.file_name)
        self.file_object = temp_path.open(mode=self.mode, buffering=self.buffering)
        return self

    def __exit__(self, exc, value, tb):
        self.file_object.close()
        super().__exit__(exc, value, tb)
