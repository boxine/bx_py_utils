from pathlib import Path

import pytest

import bx_py_utils
from bx_py_utils.auto_doc import ModulePath, assert_readme, generate_modules_doc


BASE_PATH = Path(bx_py_utils.__file__).parent


def test_module_path():
    assert ModulePath().get_base_path('bx_py_utils') == BASE_PATH
    assert ModulePath().get_base_path('bx_py_utils.auto_doc') == BASE_PATH


def test_generate_modules_doc_without_links():
    doc_block = generate_modules_doc(
        modules=['bx_py_utils.auto_doc'],
        start_level=0,
        link_template=None,
    )
    assert '* `assert_readme()` - Check and update README' in doc_block


def test_generate_modules_doc_with_links():
    doc_block = generate_modules_doc(
        modules=['bx_py_utils.auto_doc'],
        start_level=0,
        link_template='https://test.tld/blob/master/{path}#L{start}-L{end}',
    )
    assert (
        '* [`assert_readme()`](https://test.tld/blob/master/bx_py_utils/auto_doc.py#L111-L151)'
        ' - Check'
    ) in doc_block


def test_auto_doc_in_readme():
    readme_path = BASE_PATH.parent / 'README.md'

    assert_readme(
        readme_path=readme_path,
        modules=['bx_py_utils'],
        start_marker_line='[comment]: <> (✂✂✂ auto generated start ✂✂✂)',
        end_marker_line='[comment]: <> (✂✂✂ auto generated end ✂✂✂)',
        start_level=2,
        link_template='https://github.com/boxine/bx_py_utils/blob/master/{path}#L{start}-L{end}'
    )


def test_old_link_template_pattern():
    with pytest.deprecated_call(match=(
        '"lnum" in "link_template" will be removed in the future. Change it to "start"'
    )):
        doc_block = generate_modules_doc(
            modules=['bx_py_utils.auto_doc'],
            start_level=0,
            link_template='https://test.tld/blob/master/{path}#L{lnum}',
        )
        assert doc_block
    assert (
        '* [`assert_readme()`](https://test.tld/blob/master/bx_py_utils/auto_doc.py#L111) - Check'
    ) in doc_block
