import unittest

from bs4 import BeautifulSoup

from sec_html_parser.parser import Parser


class TestParser(unittest.TestCase):
    def test_parser_creation(self):
        p = Parser()

    def test_is_child_size_larger(self):
        child = BeautifulSoup('<span style="font-size:9pt"', features="html.parser")
        child = list(child.children)[0]
        parent = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
        parent = list(parent.children)[0]

        p = Parser()
        self.assertTrue(p._is_child(child, parent))
        self.assertFalse(p._is_child(parent, child))

    def test_is_child_size_equal(self):
        sibling1 = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
        sibling1 = list(sibling1.children)[0]
        sibling2 = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
        sibling2 = list(sibling2.children)[0]

        p = Parser()
        self.assertFalse(p._is_child(sibling1, sibling2))
        self.assertFalse(p._is_child(sibling2, sibling1))

    def test_is_child_size_equal_weight_larger(self):
        child = BeautifulSoup(
            '<span style="font-size:10pt;font-weight:400"', features="html.parser"
        )
        child = list(child.children)[0]
        parent = BeautifulSoup(
            '<span style="font-size:10pt;font-weight:700"', features="html.parser"
        )
        parent = list(parent.children)[0]

        p = Parser()
        self.assertTrue(p._is_child(child, parent))
        self.assertFalse(p._is_child(parent, child))

    def test_is_child_size_equal_weight_equal(self):
        sibling1 = BeautifulSoup(
            '<span style="font-size:10pt;font-weight:400"', features="html.parser"
        )
        sibling1 = list(sibling1.children)[0]
        sibling2 = BeautifulSoup(
            '<span style="font-size:10pt;font-weight:400"', features="html.parser"
        )
        sibling2 = list(sibling2.children)[0]

        p = Parser()
        self.assertFalse(p._is_child(sibling1, sibling2))
        self.assertFalse(p._is_child(sibling2, sibling1))

    def test_is_child_size_equal_weight_equal_style_italic(self):
        child = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">iPhone</span>""",
            features="html.parser",
        )
        child = list(child.children)[0]
        parent = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>""",
            features="html.parser",
        )
        parent = list(parent.children)[0]

        p = Parser()
        self.assertTrue(p._is_child(child, parent))
        self.assertFalse(p._is_child(parent, child))

    def test_is_child_size_equal_weight_equal_style_equal(self):
        sibling1 = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>""",
            features="html.parser",
        )
        sibling1 = list(sibling1.children)[0]
        sibling2 = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>""",
            features="html.parser",
        )
        sibling2 = list(sibling2.children)[0]

        p = Parser()
        self.assertFalse(p._is_child(sibling1, sibling2))
        self.assertFalse(p._is_child(sibling2, sibling1))
