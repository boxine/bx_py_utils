import inspect
from unittest.mock import patch

import pytest

from bx_py_utils import html_utils
from bx_py_utils.html_utils import InvalidHtml, pretty_format_html, validate_html


def test_validate_html():
    validate_html('<p>Test</p>')
    validate_html('<a><b/></a>')

    # Validator accept any tags, not only known one:
    validate_html('<foo><bar/></foo>')
    validate_html('<nav class="sticky" id="nav-sidebar"></nav>')

    with pytest.raises(InvalidHtml) as exc_info:
        validate_html(inspect.cleandoc('''
            <no-html>
                <foo>
                    <bar>
                        <h1>Test</h1>
                        <p> >broken< </p>
                        <p>the end</p>
                    <bar>
                </foo>
            </no-html>
        '''))
    error_message = str(exc_info.value)
    print(error_message)
    assert error_message == inspect.cleandoc('''
        StartTag: invalid element name, line 5, column 25
        --------------------------------------------------------------------------------
        02     <foo>
        03         <bar>
        04             <h1>Test</h1>
        05             <p> >broken< </p>
        ----------------------------^
        06             <p>the end</p>
        07         <bar>
        08     </foo>
        --------------------------------------------------------------------------------
    ''')

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