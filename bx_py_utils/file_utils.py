import hashlib
import io
import tempfile
from pathlib import Path
from typing import BinaryIO, Iterable


class FileError(AssertionError):
    """
    Base error class for all 'file_utils' exceptions.
    """

    pass


class EmptyFileError(FileError):
    """
    Will be raised from get_and_assert_file_size() if a 0-bytes file was found.
    """
    pass


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

    def __init__(self, hash_names: Iterable = None):
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

    Note:
        seek() is not implemented,
        because the on-the-fly hash calculation requires a linear writing
    """

    def __init__(
        self,
        file_name: str,
        hash_names: Iterable = None,
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
        self.temp_file.file_object.write(data)
        self.hasher(data)

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

        bytes_processed = self.hasher.bytes_processed
        if self.avoid_empty_files and not bytes_processed:
            raise EmptyFileError(f'Nothing written to: {self.file_name!r}')

        if self.expected_files_size and bytes_processed != self.expected_files_size:
            raise FileSizeError(
                file_name=self.file_name,
                current_size=bytes_processed,
                expected_size=self.expected_files_size,
            )
