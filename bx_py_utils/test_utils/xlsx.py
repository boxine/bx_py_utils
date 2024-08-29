import io
from collections.abc import Generator
from itertools import zip_longest

from bx_py_utils.dict_utils import dict_list2markdown
from bx_py_utils.test_utils.context_managers import MassContextManager
from bx_py_utils.test_utils.zip_file_utils import FreezeZipFileDatetime, zip_info_markdown


try:
    import openpyxl
except ImportError as err:
    openpyxl = None
    openpyxl_import_error = err
else:
    openpyxl_import_error = None

try:
    from freezegun import freeze_time
except ImportError as err:
    freeze_time = None
    freeze_time_import_error = err
else:
    freeze_time_import_error = None


def xlsx2dict(xlsx: bytes) -> dict:
    """
    Convert a XLSX file content into a dictionary: Every sheet is a key, and the value is a list of dictionaries.
    Interesting to make snapshots of Excel files ;)
    """
    assert openpyxl, f'openpyxl is needed: {openpyxl_import_error}'

    wb = openpyxl.load_workbook(io.BytesIO(xlsx), read_only=True)
    table_data = {}
    for sheet in wb.worksheets:
        sheet_data = []
        keys = None
        for row in sheet.rows:
            if keys is None:
                keys = [cell.value for cell in row]
            else:
                row_data = {
                    key or f'UnnamedColumn{index}': cell.value
                    for index, (key, cell) in enumerate(zip_longest(keys, row), start=1)
                }
                sheet_data.append(row_data)

        table_data[sheet.title] = sheet_data

    return table_data


def xlsx2markdown(xlsx: bytes, header: str = '#') -> Generator[str]:
    """
    Convert all Sheets of a XLSX into markdown tables.
    Interesting to make snapshots of Excel files ;)
    """
    for sheet_name, sheet_data in xlsx2dict(xlsx).items():
        yield f'{header} {sheet_name}'
        if sheet_data:
            yield from dict_list2markdown(sheet_data)
        else:
            yield '(No data in sheet)'
        yield ''


def generate_xlsx_md_snapshot(xlsx: bytes) -> str:
    """
    Generate a markdown snapshot of a XLSX: Display ZIP info + Sheets content as Markdown.
    Usage e.g.:
        assert_text_snapshot(got=generate_xlsx_md_snapshot(xlsx_data), extension='.md')
    """

    def generate(xlsx):
        yield '# ZIP Info:'
        yield zip_info_markdown(xlsx)
        yield '# Content of all Sheets:'
        yield from xlsx2markdown(xlsx, header='##')

    return '\n'.join(generate(xlsx))


class FreezeXlsxTimes(MassContextManager):
    """
    Context manager / decorator intended to freeze timestamps of xlsx files creation by e.g.: openpyxl.
    (e.g.: Helps to create reproducible openpyxl files for tests)
    """

    def __init__(self, dt_str: str = '2024-12-24T00:00:00+00:00'):
        if freeze_time is None:
            raise ImportError(f'freezegun is needed: {freeze_time_import_error}')

        self.mocks = (
            freeze_time(dt_str),
            FreezeZipFileDatetime(dt_str),
        )
