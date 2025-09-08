from unittest import TestCase
from unittest.mock import call, patch

from bx_py_utils.import_utils import import_all_files
from bx_py_utils.path import MockCurrentWorkDir


class ImportAllFilesTests(TestCase):
    def test_import_all_files(self):
        with (
            MockCurrentWorkDir(prefix='test_import_all_files') as temp_cwd,
            patch('bx_py_utils.import_utils.import_module') as mock_import,
        ):
            temp_path = temp_cwd.temp_path / 'mypackage'
            temp_path.mkdir()

            init_file_path = temp_path / '__init__.py'
            init_file_path.touch()

            (temp_path / 'a.py').write_text('# foo')
            (temp_path / 'b.py').write_text('# bar')
            (temp_path / '_private.py').write_text('# baz')

            imported = import_all_files(package=temp_path.name, init_file=str(init_file_path))

        self.assertEqual(imported, ['mypackage.a', 'mypackage.b'])
        self.assertEqual(mock_import.call_args_list, [call('mypackage.a'), call('mypackage.b')])
