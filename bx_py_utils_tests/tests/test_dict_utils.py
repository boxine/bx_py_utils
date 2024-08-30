import inspect
from collections.abc import Generator
from unittest import TestCase

from bx_py_utils.dict_utils import dict_list2markdown


class DictUtilsTestCase(TestCase):
    def assert_dict_list2markdown(self, data, expected):
        result = dict_list2markdown(data)
        self.assertIsInstance(result, Generator)
        markdown = '\n'.join(result)
        expected = inspect.cleandoc(expected)
        self.assertEqual(markdown, expected)

    def test_dict_list2markdown(self):
        self.assert_dict_list2markdown(
            data=[
                {'a': 'A1', 'b': 'B1'},
                {'a': 'A2', 'b': 'B2'},
                {'a': 'A3', 'b': 'B3'},
            ],
            expected="""
                | index | a | b |
                | ----- | ----- | ----- |
                | 1 | A1 | B1 |
                | 2 | A2 | B2 |
                | 3 | A3 | B3 |
            """,
        )

    def test_dict_list2markdown_newlines(self):
        self.assert_dict_list2markdown(
            data=[
                {'New Lines': 'Line\nFeed'},
                {'New Lines': 'Carriage\rReturn'},
                {'New Lines': 'Carriage Return\r\nand\r\nLine Feed'},
            ],
            expected="""
                | index | New Lines |
                | ----- | ----- |
                | 1 | Line<br>Feed |
                | 2 | Carriage<br>Return |
                | 3 | Carriage Return<br>and<br>Line Feed |
            """,
        )
        self.assert_dict_list2markdown(
            data=[
                {'Line\nFeed': 'A1', 'Carriage\rReturn': 'B1', 'Carriage Return\r\nand\r\nLine Feed': 'C1'},
            ],
            expected="""
                | index | Line<br>Feed | Carriage<br>Return | Carriage Return<br>and<br>Line Feed |
                | ----- | ----- | ----- | ----- |
                | 1 | A1 | B1 | C1 |
            """,
        )

    def test_dict_list2markdown_escaping(self):
        self.assert_dict_list2markdown(
            data=[
                {'Escape': 'Foo|Bar|Baz'},
            ],
            expected=r"""
                | index | Escape |
                | ----- | ----- |
                | 1 | Foo\|Bar\|Baz |
            """,
        )
        self.assert_dict_list2markdown(
            data=[
                {'Foo|Bar|Baz': 'A1'},
            ],
            expected=r"""
                | index | Foo\|Bar\|Baz |
                | ----- | ----- |
                | 1 | A1 |
            """,
        )
