import inspect
from unittest import TestCase
from unittest.mock import patch

from bx_py_utils import html_utils
from bx_py_utils.html_utils import InvalidHtml, pretty_format_html, validate_html


class HtmlUtilsTestCase(TestCase):
    def test_validate_html(self):
        validate_html('<p>Test</p>')
        validate_html('<a><b/></a>')

        # Validator accept any tags, not only known one:
        validate_html('<foo><bar/></foo>')
        validate_html('<nav class="sticky" id="nav-sidebar"></nav>')

        with self.assertRaises(InvalidHtml) as exc_info:
            validate_html(
                inspect.cleandoc(
                    '''
                    <no-html>
                        <foo>
                            <bar>
                                <h1>Test</h1>
                                <p> >broken< </p>
                                <p>the end</p>
                            <bar>
                        </foo>
                    </no-html>
                '''
                )
            )
        error_message = str(exc_info.exception)
        self.assertEqual(
            error_message,
            inspect.cleandoc(
                '''
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
                '''
            ),
        )

        # Our helpful error message if requirements missing?

        with patch.object(html_utils, 'html', None), self.assertRaises(ModuleNotFoundError) as cm:
            validate_html('')

        self.assertEqual(
            cm.exception.args,
            ('This feature needs "lxml", please add it to you requirements',),
        )

    def test_pretty_format_html(self):
        self.assertEqual(pretty_format_html('<p>Test</p>'), '<p>\n Test\n</p>')

        html = pretty_format_html(
            '''
             \r\n <h1>X</h1> \r\n \r\n
            <p><strong>Test</strong></p> \r\n \r\n
        '''
        )
        self.assertEqual(html, '<h1>\n X\n</h1>\n<p>\n <strong>\n  Test\n </strong>\n</p>')

        self.assertEqual(
            pretty_format_html("<code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>"),
            ('<code>\n' " &lt;script&gt;alert('XSS')&lt;/script&gt;\n" '</code>'),
        )

        self.assertEqual(
            pretty_format_html('<p>&lt;XSS énc🕳d&#128065;ng&gt; a&#97;&#x61;</p>'),
            ('<p>\n &lt;XSS énc🕳d👁ng&gt; aaa\n</p>'),
        )

        # Our helpful error message if requirements missing?

        with patch.object(html_utils, 'BeautifulSoup', None), self.assertRaises(ModuleNotFoundError) as cm:
            pretty_format_html('')

        self.assertEqual(
            cm.exception.args,
            ('This feature needs "beautifulsoup4", please add it to you requirements',),
        )
