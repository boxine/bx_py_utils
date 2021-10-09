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
            f'{"-"*80}\n'
            f'{self.cutout_text}\n'
            f'{"-"*80}'
        )


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


def pretty_format_html(data, parser='html.parser', **bs_kwargs):
    """
    Pretty format given HTML document via BeautifulSoup (Needs 'beautifulsoup4' package)
    """
    assert isinstance(data, str)

    if BeautifulSoup is None:
        raise ModuleNotFoundError(
            'This feature needs "beautifulsoup4", please add it to you requirements'
        )

    soup = BeautifulSoup(data, parser, **bs_kwargs)
    return soup.prettify(
        formatter=None  # Do not perform any substitution
    )
