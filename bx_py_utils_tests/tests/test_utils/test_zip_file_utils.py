import datetime
import io
import tempfile
import zipfile
from pathlib import Path
from unittest import TestCase

from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from bx_py_utils.test_utils.zip_file_utils import FreezeZipFileDatetime, ZipFileInfo, zip_info, zip_info_markdown


def generate_example_zip_file() -> io.BytesIO:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_LZMA) as zf:
            for number in range(1, 3):
                file_path = temp_path / f'file{number}.txt'
                file_path.write_text(f'Just a {"test file" * (number * 2)}\n')
                zf.write(file_path, arcname=file_path.name)

    zip_file.seek(0)
    return zip_file


class ZipFileUtilsTestCase(TestCase):
    maxDiff = None

    def test_freeze_zip_file_datetime(self):
        with FreezeZipFileDatetime('2024-12-24T00:00:00+00:00'):
            zip_file = generate_example_zip_file()

        with zipfile.ZipFile(zip_file, 'r') as zf:
            zip_info = [
                (
                    info.filename,
                    datetime.datetime(*info.date_time).astimezone(datetime.timezone.utc).isoformat(),
                )
                for info in zf.infolist()
            ]
        self.assertEqual(
            zip_info,
            [
                ('file1.txt', '2024-12-24T00:00:00+00:00'),
                ('file2.txt', '2024-12-24T00:00:00+00:00'),
            ],
        )

    def test_zip_info(self):
        with FreezeZipFileDatetime():
            zip_file = generate_example_zip_file()

        info = list(zip_info(zip_file))  # Consumes the generator
        self.assertEqual(
            info,
            [
                ZipFileInfo(
                    file_size=26,
                    compress_size=37,
                    compress_ratio=142,
                    compress_type='lzma',
                    modification_date='2024-12-24T00:00:00+00:00',
                    crc32='5BDCF848',
                    file_name='file1.txt',
                ),
                ZipFileInfo(
                    file_size=44,
                    compress_size=38,
                    compress_ratio=86,
                    compress_type='lzma',
                    modification_date='2024-12-24T00:00:00+00:00',
                    crc32='06545222',
                    file_name='file2.txt',
                ),
            ],
        )

        assert_text_snapshot(got=zip_info_markdown(zip_file), extension='.md')
