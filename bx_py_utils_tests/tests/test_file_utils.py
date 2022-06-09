import io
from pathlib import Path
from unittest import TestCase

from bx_py_utils.file_utils import (
    EmptyFileError,
    FileHasher,
    FileSizeError,
    NamedTemporaryFile2,
    TempFileHasher,
    get_and_assert_file_size,
)


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

    def test_file_hasher(self):
        with FileHasher() as file_hasher:
            assert file_hasher.bytes_processed == 0
            file_hasher(b'123')
        assert file_hasher.bytes_processed == 3
        assert file_hasher.hexdigest_dict() == {
            'md5': '202cb962ac59075b964b07152d234b70',
            'sha1': '40bd001563085fc35165329ea1ff5c5ecbdbbeef',
            'sha3_224': '602bdc204140db016bee5374895e5568ce422fabe17e064061d80097',
        }

        with FileHasher(hash_names=('md5',)) as file_hasher:
            file_hasher(b'12')
            assert file_hasher.bytes_processed == 2
            file_hasher(b'3')
            assert file_hasher.bytes_processed == 3
        assert file_hasher.hexdigest_dict() == {'md5': '202cb962ac59075b964b07152d234b70'}

        with self.assertRaises(ValueError) as err:
            FileHasher(hash_names=('Bam!',))
        msg = str(err.exception)
        assert msg == 'unsupported hash type Bam!'

    def test_temp_file_hasher(self):
        with TempFileHasher(file_name='foo.bar', expected_files_size=3) as tfh:
            assert not hasattr(tfh, 'seek')  # seek() should not be supported!
            tfh.write(b'123')

            file_object = tfh.temp_file.file_object
            path = Path(file_object.name)
            assert path.name == 'foo.bar'

            assert tfh.closed is False
            assert tfh.tell() == tfh.hasher.bytes_processed == 3

        assert tfh.closed is True
        assert tfh.hasher.hexdigest_dict() == {
            'md5': '202cb962ac59075b964b07152d234b70',
            'sha1': '40bd001563085fc35165329ea1ff5c5ecbdbbeef',
            'sha3_224': '602bdc204140db016bee5374895e5568ce422fabe17e064061d80097',
        }

        with self.assertRaises(FileSizeError) as err:
            with TempFileHasher(
                file_name='foo.bar', hash_names=('md5',), expected_files_size=99
            ) as tfh:
                tfh.write(b'12')
                tfh.write(b'3')
            assert tfh.hasher.hexdigest_dict() == {'md5': '202cb962ac59075b964b07152d234b70'}
        msg = str(err.exception)
        assert msg == "File 'foo.bar' is 3 Bytes in size, but should be 99 Bytes!"
