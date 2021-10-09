try:
    from lxml import html  # lxml is optional requirement
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
    Exception class used in validate_html() on HTML parse/validate error.
    """
    pass


def validate_html(data):
    """
    Validate a HTML document (Needs 'lxml' package)

    There are a few more ways to validate HTML documents,
    but the intention here is just to raise an error on
    really broken documents.
    """
    assert isinstance(data, str)

    if html is None:
        raise ModuleNotFoundError(
            'This feature needs "lxml", please add it to you requirements'
        )

    parser = html.HTMLParser(
        recover=False,  # Crash faster on broken HTML
    )
    try:
        parser.feed(data)
        parser.close()
    except XMLSyntaxError as err:
        raise InvalidHtml(err)


def pretty_format_html(data):
    """
    Pretty format given HTML document via BeautifulSoup (Needs 'beautifulsoup4' package)
    """
    assert isinstance(data, str)

    if BeautifulSoup is None:
        raise ModuleNotFoundError(
            'This feature needs "beautifulsoup4", please add it to you requirements'
        )

    soup = BeautifulSoup(data, 'html.parser')
    return soup.prettify(
        formatter=None  # Do not perform any substitution
    )
