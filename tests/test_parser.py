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
