from bs4 import BeautifulSoup

from sec_html_parser.span_style import SpanStyle


def test_span_style():
    span_style = "color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%"
    span_style = SpanStyle(span_style)
    assert span_style.size == 9
    assert span_style.weight == 400
    assert span_style.style == "italic"
    assert span_style.relative is False


def test_span_style_from_node():
    soup = BeautifulSoup(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%"></span>""",
        features="html.parser",
    )
    span_node = list(soup.children)[0]
    span_style = SpanStyle(span_node)
    assert span_style.size == 9
    assert span_style.weight == 400
    assert span_style.style == "italic"
    assert span_style.relative is False


def test_span_style_from_node_relative():
    soup = BeautifulSoup(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:6.5pt;font-weight:400;line-height:120%;position:relative;top:-3.5pt;vertical-align:baseline">Â®</span>""",
        features="html.parser",
    )
    span_node = list(soup.children)[0]
    span_style = SpanStyle(span_node)
    assert span_style.size == 6.5
    assert span_style.weight == 400
    assert span_style.style is None
    assert span_style.relative is True
