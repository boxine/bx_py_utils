import inspect
from unittest import TestCase
from unittest.mock import patch

import typeguard

from bx_py_utils import html_utils
from bx_py_utils.html_utils import (
    InvalidHtml,
    _strip_html_once,
    html2text,
    pretty_format_html,
    strip_html_tags,
    validate_html,
)


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


class StripHtmlTagsTests(TestCase):
    def test_basics(self):
        self.assertEqual(strip_html_tags('<foo>bar</foo>'), 'bar')
        self.assertEqual(strip_html_tags('foo&nbsp;&amp;&nbsp;bar'), 'foo\xa0&\xa0bar')
        self.assertEqual(strip_html_tags('foo&#169;bar'), 'foo\xa9bar')
        self.assertEqual(strip_html_tags('foo&#x2764;bar'), 'foo❤bar')
        self.assertEqual(strip_html_tags('   foo    '), 'foo')
        self.assertEqual(strip_html_tags('  foo  bar  '), 'foo bar')
        self.assertEqual(strip_html_tags('<!-- no --> <x>foo<y>bar'), 'foobar')
        self.assertEqual(strip_html_tags('<p>1 &lt; 2</p>'), '1 < 2')
        self.assertEqual(strip_html_tags('<script'), '')

    def test_non_string_raises(self):
        with typeguard.suppress_type_checks(), self.assertRaises(AssertionError):
            strip_html_tags(None)
        with typeguard.suppress_type_checks(), self.assertRaises(AssertionError):
            strip_html_tags(42)

    def test_double_execution_loop(self):
        # HTMLParser misses tags on first pass (e.g. inside <style> blocks)
        test_code = '1&amp;2</p><style><!-- removed in second run --></style>'

        first_run = _strip_html_once(test_code, keep_paragraphs=True)
        self.assertEqual(first_run, '1&2\n<!-- removed in second run -->')

        second_run = _strip_html_once(first_run, keep_paragraphs=True)
        self.assertEqual(second_run, '1&2')

        self.assertEqual(strip_html_tags(test_code, keep_paragraphs=True), '1&2')

    def test_paragraphs(self):
        self.assertEqual(strip_html_tags(' \n foo \n bar \n ', keep_paragraphs=True), 'foo\nbar')
        self.assertEqual(strip_html_tags(' \n foo \n bar \n ', keep_paragraphs=False), 'foo bar')

        self.assertEqual(
            strip_html_tags(' \t\r\f\v\n foo \t\r\f\v\n bar \t\r\f\v\n ', keep_paragraphs=True),
            'foo\nbar',
        )
        self.assertEqual(
            strip_html_tags(' \t\r\f\v\n foo \t\r\f\v\n bar \t\r\f\v\n ', keep_paragraphs=False),
            'foo bar',
        )

        self.assertEqual(strip_html_tags(' \n\n foo \n\n bar \n\n ', keep_paragraphs=True), 'foo\n\nbar')
        self.assertEqual(strip_html_tags(' \n\n foo \n\n bar \n\n ', keep_paragraphs=False), 'foo bar')

        self.assertEqual(strip_html_tags('<p>foo</p><p>bar</p>', keep_paragraphs=True), 'foo\nbar')
        self.assertEqual(strip_html_tags('\n<p>foo</p>\n<p>bar</p>\n', keep_paragraphs=True), 'foo\n\nbar')
        self.assertEqual(strip_html_tags('<p>foo</p><p>bar</p>', keep_paragraphs=False), 'foo bar')
        self.assertEqual(
            strip_html_tags('<p>foo\n</p><p>\n</p><p>bar\n</p>', keep_paragraphs=False),
            'foo bar',
        )

    def test_li_bullet(self):
        self.assertEqual(strip_html_tags('<ul><li>a</li><li>b</li></ul>'), '· a · b')


class Html2TextTests(TestCase):
    def test_basic_paragraphs(self):
        self.assertEqual(html2text('foo\nbar\n'), 'foo bar')
        self.assertEqual(html2text('line1\n\nline2\n'), 'line1\n\nline2')
        self.assertEqual(html2text('line1\r\n\r\nline2\r\n'), 'line1\n\nline2')
        self.assertEqual(html2text('line1\r\rline2\r'), 'line1\n\nline2')
        self.assertEqual(html2text('foo\n\n\nbar\n'), 'foo\n\nbar')
        self.assertEqual(html2text('foo\n\n\n\nbar\n'), 'foo\n\nbar')

    def test_p_tags(self):
        self.assertEqual(html2text('<p>foo</p><p>bar</p>'), 'foo bar')
        self.assertEqual(html2text('<p>foo</p><p></p><p>bar</p>'), 'foo\n\nbar')

    def test_multiline_html(self):
        value = '<p>intro sentence<p>\n\n<p><p>\n\n<p>description\nfoo\n\t\r\n\f\v\n\nbar</p>\n\n\n'
        self.assertEqual(html2text(value), 'intro sentence\n\ndescription foo\n\nbar')

    def test_non_string_raises(self):
        with typeguard.suppress_type_checks(), self.assertRaises(AssertionError):
            html2text(None)
