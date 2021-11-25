import io
from pathlib import Path
from unittest import TestCase

from bx_py_utils.file_utils import EmptyFileError, NamedTemporaryFile2, get_and_assert_file_size


class TempFileUtilsTestCase(TestCase):
    def test_get_and_assert_file_size(self):
        file_object = io.BytesIO()
        with self.assertRaises(EmptyFileError) as cm:
            get_and_assert_file_size(file_object, msg='Test 1')
        assert cm.exception.args[0] == 'Empty file error: Test 1'

        file_object.write(b'1234')
        file_size = get_and_assert_file_size(file_object, msg='Test 2')
        assert file_size == 4

    def test_names_temporary_file(self):
        with NamedTemporaryFile2(file_name='file.ext') as temp_cm1:
            assert temp_cm1.file_name == 'file.ext'
            temp1_path = Path(temp_cm1.file_object.name)
            assert temp1_path.is_file()
            assert temp1_path.parent.is_dir()
            assert temp1_path.name == 'file.ext'
            temp_cm1.file_object.write(b'temp 1')
            temp_cm1.file_object.flush()
            assert temp1_path.read_bytes() == b'temp 1'

            # Create a second temp file with the **same** name:

            with NamedTemporaryFile2(file_name='file.ext') as temp_cm2:
                assert temp_cm2.file_name == 'file.ext'  # same as temp1!
                temp2_path = Path(temp_cm2.file_object.name)
                assert temp2_path.is_file()
                assert temp2_path.parent.is_dir()
                assert temp1_path != temp2_path

                assert temp2_path.name == 'file.ext'  # same as temp1!
                temp_cm2.file_object.write(b'temp 2')
                temp_cm2.file_object.flush()
                assert temp2_path.read_bytes() == b'temp 2'

            assert temp2_path.exists() is False
            assert temp2_path.parent.exists() is False  # created temp directory removed, too?
            assert temp1_path.read_bytes() == b'temp 1'

        assert temp1_path.exists() is False
        assert temp1_path.parent.exists() is False  # created temp directory removed, too?
