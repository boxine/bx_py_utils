import tempfile
from pathlib import Path
from unittest import TestCase

from bx_py_utils.test_utils.filesystem_utils import FileWatcher


class FilesystemTestUtilsTestCase(TestCase):
    def test_file_watcher(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_path = Path(tmp_dir)

            # Create some files before enter the context manager:
            initial_items = {Path(temp_path, 'test_1.txt'), Path(temp_path, 'test_2.txt')}
            [item.touch() for item in initial_items]

            with FileWatcher(base_path=temp_path, cleanup=True) as file_watcher:
                # Only initial items there?
                assert file_watcher._get_items() == initial_items
                assert file_watcher.get_new_items() == set()

                # Create some new files:
                new_items = {Path(temp_path, 'test_3.txt'), Path(temp_path, 'test_4.txt')}
                [item.touch() for item in new_items]

                # All files collected?
                assert file_watcher._get_items() == initial_items | new_items
                assert file_watcher.get_new_items() == new_items

            # cleanup made? New files removed?
            assert set(temp_path.glob('*')) == initial_items
