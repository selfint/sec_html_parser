import unittest

from bs4 import BeautifulSoup

from sec_html_parser.font_style import FontStyle


class TestFontStyle(unittest.TestCase):
    def test_font_style(self):
        span_style = "color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%"
        font_style = FontStyle(span_style)
        assert font_style.size == 9
        assert font_style.weight == 400
        assert font_style.style == "italic"
        assert font_style.relative == False

    def test_font_style_from_node(self):
        soup = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%"></span>""",
            features="html.parser",
        )
        span_node = list(soup.children)[0]
        font_style = FontStyle(span_node)
        assert font_style.size == 9
        assert font_style.weight == 400
        assert font_style.style == "italic"
        assert font_style.relative == False

    def test_font_style_from_node_relative(self):
        soup = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:6.5pt;font-weight:400;line-height:120%;position:relative;top:-3.5pt;vertical-align:baseline">Â®</span>""",
            features="html.parser",
        )
        span_node = list(soup.children)[0]
        font_style = FontStyle(span_node)
        assert font_style.size == 6.5
        assert font_style.weight == 400
        assert font_style.style == None
        assert font_style.relative == True
