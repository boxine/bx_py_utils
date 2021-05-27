import inspect
from pathlib import Path
from typing import Union

from bx_py_utils.path import assert_is_file


class FrameNotFound(LookupError):
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def __str__(self):
        return f'Frame outside "{self.file_path}" not found!'


def last_frame_outside_path(file_path: Union[Path, str]):
    """
    Returns the stack frame that is the direct successor of given "file_path".
    The use case may be to find caller information.

    raise FrameNotFound if the given file path is not in stack.
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    assert_is_file(file_path)

    frames = inspect.stack()
    if frames is None:
        # Maybe we don't run via CPython?!?
        raise RuntimeError(
            'Can not get stack frame. Current interpreter has no support for them?'
        )

    match_path = False
    for frame in frames:
        frame_path = Path(frame.filename)

        if frame_path == file_path:
            match_path = True
        elif match_path:
            return frame

    raise FrameNotFound(file_path)
