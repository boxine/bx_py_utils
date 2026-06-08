import html as _html
import re
from html.parser import HTMLParser

from bx_py_utils.string_utils import ensure_lf
from bx_py_utils.text_tools import cutout


try:
    from lxml import etree, html  # lxml is optional requirement
except ModuleNotFoundError:
    html = None
else:
    from lxml.etree import XMLSyntaxError


try:
    from bs4 import BeautifulSoup  # BeautifulSoup4 is optional requirement
except ModuleNotFoundError:
    BeautifulSoup = None


class InvalidHtml(AssertionError):
    """
    XMLSyntaxError with better error messages: used in validate_html()
    """

    def __init__(self, *args):
        self.args = args

        data, origin_err = args
        assert isinstance(data, str)
        assert isinstance(origin_err, XMLSyntaxError)

        self.origin_msg = origin_err.msg

        line_no, column = origin_err.position
        self.cutout_text = cutout(data, line_no, column, extra_lines=3)

    def __str__(self):
        return (
            f'{self.origin_msg}\n'
            f'{"-" * 80}\n'
            f'{self.cutout_text}\n'
            f'{"-" * 80}'
        )


class ElementsNotFoundError(AssertionError):
    """
    Happens if requested HTML elements cannot be found
    """
    pass


def validate_html(data, **parser_kwargs):
    """
    Validate a HTML document via XMLParser (Needs 'lxml' package)

    There are a few more ways to validate HTML documents,
    but the intention here is just to raise an error on
    really broken documents.

    To be more strict set "recover=False"
    """
    assert isinstance(data, str)

    if html is None:
        raise ModuleNotFoundError(
            'This feature needs "lxml", please add it to you requirements'
        )

    parser = etree.XMLParser(**parser_kwargs)
    try:
        parser.feed(data)
        parser.close()
    except XMLSyntaxError as err:
        raise InvalidHtml(data, err)


def get_beautiful_soup_instance(data, parser='html.parser', **bs_kwargs):
    assert isinstance(data, str)

    if BeautifulSoup is None:
        raise ModuleNotFoundError(
            'This feature needs "beautifulsoup4", please add it to you requirements'
        )

    return BeautifulSoup(data, parser, **bs_kwargs)


def pretty_format_html(data, parser='html.parser', **bs_kwargs):
    """
    Pretty format given HTML document via BeautifulSoup (Needs 'beautifulsoup4' package)
    """
    soup = get_beautiful_soup_instance(data, parser, **bs_kwargs)
    return soup.prettify().rstrip()


def get_html_elements(data, query_selector, parser='html.parser', **bs_kwargs):
    """
    Returns the selected HTML elements as string
    """
    soup = get_beautiful_soup_instance(data, parser, **bs_kwargs)
    selected_elements = soup.select(query_selector)

    if not selected_elements:
        raise ElementsNotFoundError(
            f'The query selector {query_selector} did not match any element in the HTML document'
        )

    return ''.join(str(tag) for tag in selected_elements)


class _HTMLStripper(HTMLParser):
    def __init__(self, keep_paragraphs):
        self.keep_paragraphs = keep_paragraphs
        super().__init__(convert_charrefs=False)
        self.fed = []

    def handle_data(self, d):
        d = re.sub(r'[\t\r\f\v]', ' ', d)
        self.fed.append(d)

    def handle_entityref(self, name):
        self.fed.append(_html.unescape(f'&{name};'))

    def handle_charref(self, name):
        self.fed.append(_html.unescape(f'&#{name};'))

    def handle_starttag(self, tag, attributes):
        if tag == 'li':
            self.fed.append('· ')
        super().handle_starttag(tag, attributes)

    def handle_endtag(self, tag):
        if self.keep_paragraphs and tag == 'p':
            self.fed.append('\n')
        else:
            self.fed.append(' ')

    def get_data(self):
        data = ''.join(self.fed)
        data = re.sub(r'[ ]{2,}', ' ', data)
        if self.keep_paragraphs:
            data = '\n'.join(line.strip() for line in data.splitlines())
        else:
            data = ' '.join(line.strip() for line in data.splitlines() if line.strip())
            data = re.sub(r'\s{2,}', ' ', data)

        data = re.sub(r'(\n{2})\n+', r'\1', data)
        data = data.strip()
        return data


def _strip_html_once(value: str, *, keep_paragraphs: bool) -> str:
    s = _HTMLStripper(keep_paragraphs)
    s.feed(value)
    s.close()
    return s.get_data()


def strip_html_tags(value: str, *, keep_paragraphs: bool = False) -> str:
    """
    Remove HTML tags from a string using stdlib HTMLParser.

    Runs the parser in a loop until no more tags are detected, because
    HTMLParser can miss tags on the first pass (e.g. inside <style> blocks).

    >>> strip_html_tags('<p>Hello <b>World</b></p>')
    'Hello World'
    >>> strip_html_tags('<p>First</p><p>Second</p>', keep_paragraphs=True)
    'First\\nSecond'
    """
    assert isinstance(value, str), f'Expected a string, got {type(value).__name__}'
    value = _strip_html_once(value, keep_paragraphs=keep_paragraphs)
    while '<' in value and '>' in value:
        new_value = _strip_html_once(value, keep_paragraphs=keep_paragraphs)
        if new_value == value:
            # no progress — remaining '<' / '>' are not HTML tags -> exit loop
            break
        value = new_value
    return value


def html2text(value: str) -> str:
    """
    Convert HTML to plain text, preserving paragraph breaks as double newlines.

    >>> html2text('<p>First</p>\\n\\n<p>Second</p>')
    'First\\n\\nSecond'
    """
    assert isinstance(value, str), f'Expected a string, got {type(value).__name__}'
    text = ensure_lf(value)
    text = strip_html_tags(text, keep_paragraphs=True)  # preserve paragraphs as newlines
    parts = re.split(r'\n{2,}', text)
    parts = (
        strip_html_tags(part, keep_paragraphs=False)  # remove any remaining tags and extra whitespace from each part
        for part in parts
    )
    return '\n\n'.join(parts)
