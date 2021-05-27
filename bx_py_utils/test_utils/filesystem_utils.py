from pathlib import Path

from bx_py_utils.path import assert_is_dir


class FileWatcher:
    """
    Helper to record which new files have been created.
    Currently the focus is:
     * Watch only one directory
     * Cleanup/remove only files
    """

    def __init__(self, base_path: Path, cleanup: bool = True):
        assert isinstance(base_path, Path)
        assert_is_dir(base_path)

        self.base_path = base_path
        self.cleanup = cleanup

        self.initial_items = None

    def _get_items(self):
        items = set(self.base_path.glob('*'))
        return items

    def __enter__(self):
        self.initial_items = self._get_items()
        return self

    def get_new_items(self):
        current_items = self._get_items()
        new_items = current_items - self.initial_items
        return new_items

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cleanup:
            # Cleanup -> remove all created files
            new_items = self.get_new_items()
            errors = []
            for item in new_items:
                if item.exists():
                    try:
                        item.unlink()
                    except Exception as err:
                        errors.append(str(err))

            if errors:
                raise RuntimeError(', '.join(errors))
