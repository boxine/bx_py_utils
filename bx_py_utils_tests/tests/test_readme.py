from pathlib import Path
from unittest import TestCase

import bx_py_utils
from bx_py_utils.auto_doc import FnmatchExclude, ModulePath, assert_readme, generate_modules_doc


BASE_PATH = Path(bx_py_utils.__file__).parent


class ReadmeTestCase(TestCase):
    def test_module_path(self):
        assert ModulePath().get_base_path('bx_py_utils') == BASE_PATH
        assert ModulePath().get_base_path('bx_py_utils.auto_doc') == BASE_PATH

    def test_generate_modules_doc_without_links(self):
        doc_block = generate_modules_doc(
            modules=['bx_py_utils.auto_doc'],
            start_level=0,
            link_template=None,
        )
        assert '* `assert_readme()` - Check and update README' in doc_block

    def test_generate_modules_doc_with_links(self):
        doc_block = generate_modules_doc(
            modules=['bx_py_utils.auto_doc'],
            start_level=0,
            link_template='https://test.tld/blob/master/{path}#L{start}-L{end}',
        )
        assert ('* [`assert_readme()`](https://test.tld/blob/master/bx_py_utils/auto_doc.py#L') in doc_block

    def test_auto_doc_in_readme(self):
        readme_path = BASE_PATH.parent / 'README.md'

        assert_readme(
            readme_path=readme_path,
            modules=['bx_py_utils'],
            exclude_func=FnmatchExclude('test_*.py'),
            exclude_prefixes=('DocWrite:', '[no-doc]'),
            start_marker_line='[comment]: <> (✂✂✂ auto generated start ✂✂✂)',
            end_marker_line='[comment]: <> (✂✂✂ auto generated end ✂✂✂)',
            start_level=2,
            link_template='https://github.com/boxine/bx_py_utils/blob/master/{path}#L{start}-L{end}',
        )

    def test_old_link_template_pattern(self):
        with self.assertRaises(AssertionError) as cm:
            generate_modules_doc(
                modules=['bx_py_utils.auto_doc'],
                link_template='https://test.tld/blob/master/{path}#L{lnum}',
            )
        self.assertEqual(
            cm.exception.args,
            ('Please change "lnum" in "link_template" to {start}, {end}',),
        )

    def test_FnmatchExclude(self):
        file_list = ('foo.py', 'bar.py', 'foobar.py', 'test.py')

        exclude_func = FnmatchExclude('*bar.py')
        assert [item for item in file_list if exclude_func(item)] == ['foo.py', 'test.py']

        exclude_func = FnmatchExclude('f*.py')
        assert [item for item in file_list if exclude_func(item)] == ['bar.py', 'test.py']

        exclude_func = FnmatchExclude('f*.py', 'test.*')
        assert [item for item in file_list if exclude_func(item)] == ['bar.py']

    def test_exclude_func(self):
        doc_block = generate_modules_doc(
            modules=['bx_py_utils'],
            exclude_func=FnmatchExclude('*.py'),  # Exclude all files
        )
        assert doc_block == ''  # No files -> no doc
