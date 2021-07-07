import unittest

from sec_html_parser.parser import Parser


class TestParser(unittest.TestCase):
    def test_parser_creation(self):
        p = Parser()
