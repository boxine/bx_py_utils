from unittest.mock import patch

import pytest

from bx_py_utils import html_utils
from bx_py_utils.html_utils import InvalidHtml, pretty_format_html, validate_html


def test_validate_html():
    validate_html('<p>Test</p>')
    validate_html('<a><b/></a>')

    with pytest.raises(InvalidHtml) as exc_info:
        validate_html('<foo></bar>')
    assert str(exc_info.value.args[0]) == (
        'Tag foo invalid, line 1, column 5 (<string>, line 1)'
    )

    with pytest.raises(InvalidHtml) as exc_info:
        validate_html('<p> >broken< </p>')
    assert str(exc_info.value.args[0]) == (
        'htmlParseStartTag: invalid element name, line 1, column 13 (<string>, line 1)'
    )

    # Our helpful error message if requirements missing?

    with patch.object(html_utils, 'html', None), \
            pytest.raises(ModuleNotFoundError) as cm:
        validate_html('')

    assert str(cm.value) == (
        'This feature needs "lxml", please add it to you requirements'
    )


def test_pretty_format_html():
    assert pretty_format_html('<p>Test</p>') == '<p>\n Test\n</p>'

    html = pretty_format_html('''
         \r\n <h1>X</h1> \r\n \r\n
        <p><strong>Test</strong></p> \r\n \r\n
    ''')
    assert html == '<h1>\n X\n</h1>\n<p>\n <strong>\n  Test\n </strong>\n</p>\n'

    # Our helpful error message if requirements missing?

    with patch.object(html_utils, 'BeautifulSoup', None), \
            pytest.raises(ModuleNotFoundError) as cm:
        pretty_format_html('')

    assert str(cm.value) == (
        'This feature needs "beautifulsoup4", please add it to you requirements'
    )
