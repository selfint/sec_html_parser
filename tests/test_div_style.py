from bs4 import BeautifulSoup

from sec_html_parser.div_style import DivStyle


def test_div_style():
    span_style = "margin-top:9pt;text-align:justify"
    div_style = DivStyle(span_style)
    assert div_style.margin_top == 9


def test_div_style_from_node():
    soup = BeautifulSoup(
        """<div style="margin-top:1.5pt;text-align:justify"><span style="color:#000000;font-family:'Arial',sans-serif;font-size:10pt;font-style:italic;font-weight:700;line-height:120%">Graphics Market</span></div>""",
        features="html.parser",
    )
    span_node = list(soup.children)[0]
    div_style = DivStyle(span_node)
    assert div_style.margin_top == 1.5
