import unittest

from bs4 import BeautifulSoup

from sec_html_parser.font_style import FontStyle


class TestFontStyle(unittest.TestCase):
    def test_font_style(self):
        span_style = "color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%"
        font_style = FontStyle(span_style)
        self.assertEqual(font_style.size, 9)
        self.assertEqual(font_style.weight, 400)
        self.assertEqual(font_style.style, None)

    def test_font_style_from_node(self):
        soup = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%"></span>""",
            features="html.parser",
        )
        span_node = list(soup.children)[0]
        font_style = FontStyle(span_node)
        self.assertEqual(font_style.size, 9)
        self.assertEqual(font_style.weight, 400)
        self.assertEqual(font_style.style, "italic")
