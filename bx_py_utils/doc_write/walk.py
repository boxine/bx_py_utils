from pathlib import Path


def iter_file_path(file_paths: list[Path], rglob_pattern: str):
    for path in file_paths:
        yield from path.rglob(rglob_pattern)
