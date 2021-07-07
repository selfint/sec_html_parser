import unittest

from sec_html_parser.parser import Parser


class TestParser(unittest.TestCase):
    def test_parse_simple(self):
        html = """
    <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
    <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company designs, manufactures and markets smartphones.</span></div>
    """
        expected_structure = {
            "Company Background": "The Company designs, manufactures and markets smartphones."
        }
        parser = Parser()
        self.assertDictEqual(expected_structure, parser.parse_html_str(html))
