from __future__ import annotations

import hashlib
import io
import re
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import BinaryIO


class FileError(AssertionError):
    """
    Base error class for all 'file_utils' exceptions.
    """


class EmptyFileError(FileError):
    """
    Will be raised from get_and_assert_file_size() if a 0-bytes file was found.
    """


class FileSizeError(FileError):
    """
    File size is not the same as the expected size.
    """

    def __init__(self, file_name, current_size, expected_size):
        self.file_name = file_name
        self.current_size = current_size
        self.expected_size = expected_size

    def __str__(self):
        return (
            f'File {self.file_name!r} is {self.current_size} Bytes in size,'
            f' but should be {self.expected_size} Bytes!'
        )


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


class FileHasher:
    """
    Context Manager for generate different hashes from file content while processing a file.
    e.g.: Write content into a file in chunks and generate MD5 + SHA1
    """

    DEFAULT_HASH_NAMES = ('md5', 'sha1', 'sha3_224')

    def __init__(self, hash_names: Iterable | None = None):
        hash_names = hash_names or self.DEFAULT_HASH_NAMES
        self.hash = {hash_name: hashlib.new(hash_name) for hash_name in hash_names}
        self.bytes_processed = 0

    def __enter__(self):
        return self

    def __call__(self, chunk):
        for hash in self.hash.values():
            hash.update(chunk)
        self.bytes_processed += len(chunk)

    def __exit__(self, exc, value, tb):
        pass

    def hexdigest_dict(self):
        return {hash_name: hash.hexdigest() for hash_name, hash in self.hash.items()}


class TempFileHasher:
    """
    File like context manager that combines NamedTemporaryFile2 and FileHasher.
    Can also check the file size.
    """

    def __init__(
        self,
        file_name: str,
        hash_names: Iterable | None = None,
        avoid_empty_files=True,
        expected_files_size=None,
    ):
        self.file_name = file_name
        self.hash_names = hash_names
        self.avoid_empty_files = avoid_empty_files
        self.expected_files_size = expected_files_size

    def __enter__(self):
        self.temp_file = NamedTemporaryFile2(file_name=self.file_name).__enter__()
        self.hasher = FileHasher(hash_names=self.hash_names).__enter__()
        return self

    def read(self, *args):
        return self.temp_file.file_object.read(*args)

    def write(self, data):
        if self.tell() != self.hasher.bytes_processed:
            # We are not at the end of the file!
            raise RuntimeError(
                f'Avoid non-linear writing to "{self.file_name}",'
                f' because this will result in incorrect hashes!'
            )
        self.temp_file.file_object.write(data)
        self.hasher(data)

    def seek(self, *args, **kwargs):
        """
        Note: Going back and forward is ok as long as you jump back to the end of the file
              before the next write !
        """
        self.temp_file.file_object.seek(*args, **kwargs)

    def tell(self):
        return self.temp_file.file_object.tell()

    @property
    def closed(self):
        return self.temp_file.file_object.closed

    def close(self):
        self.temp_file.file_object.close()

    def flush(self):
        self.temp_file.file_object.flush()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_file.__exit__(exc_type, exc_val, exc_tb)
        self.hasher.__exit__(exc_type, exc_val, exc_tb)
        if exc_type:
            raise

        bytes_processed = self.hasher.bytes_processed
        if self.avoid_empty_files and not bytes_processed:
            raise EmptyFileError(f'Nothing written to: {self.file_name!r}')

        if self.expected_files_size and bytes_processed != self.expected_files_size:
            raise FileSizeError(
                file_name=self.file_name,
                current_size=bytes_processed,
                expected_size=self.expected_files_size,
            )


def safe_filename(input_str):
    """
    Makes an arbitrary input suitable to be used as a filename.
    """
    return re.sub(r'[^-_. \w]+', '_', input_str)


class OverlongFilenameError(AssertionError):
    """
    cut_filename() error: The file name can not be shortened, because sterm is to short.
    """


def cut_filename(file_name: str, max_length: int, min_name_len: int = 1) -> str:
    """
    Short the file name (and keep the last suffix). Raise OverlongFilenameError if it can't fit.

    :param file_name: The source file name to cut
    :param max_length: The maximum length of the entire file name.
    :param min_name_len: Mininmal length of the "stem" part (file name without suffix)

    e.g.:

    >>> cut_filename('0123456789_a_very_very_long_file_name.wav', max_length=11)
    '0123456.wav'
    >>> cut_filename('0123456789_a_very_very_long_file_name.wav', max_length=10)
    '012345.wav'
    """
    if len(file_name) <= max_length:
        return file_name

    assert min_name_len >= 1

    path = Path(file_name)

    suffix = path.suffix
    suffix_len = len(suffix)

    stem = path.stem
    cut_length = max_length - suffix_len
    if cut_length < min_name_len:
        raise OverlongFilenameError(
            f'File name {file_name!r} can not be shortened to {max_length} characters.'
        )
    cut_stem = stem[:cut_length]

    try:
        cut_path = path.with_stem(cut_stem)  # new in Python 3.9
    except AttributeError:
        cut_path = path.with_name(cut_stem + suffix)

    result = str(cut_path)
    assert len(result) == max_length
    return result
