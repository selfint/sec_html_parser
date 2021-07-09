import unittest

from bs4 import BeautifulSoup

from sec_html_parser.parser import Parser


class TestParser(unittest.TestCase):
    def test_parser_creation(self):
        p = Parser()

    def test_is_child_size_larger(self):
        child = BeautifulSoup('<span style="font-size:9pt"/>', features="html.parser")
        child = list(child.children)[0]
        parent = BeautifulSoup('<span style="font-size:10pt"/>', features="html.parser")
        parent = list(parent.children)[0]

        p = Parser()
        self.assertTrue(p._is_span_child(child, parent))
        self.assertFalse(p._is_span_child(parent, child))

    def test_is_child_size_equal(self):
        sibling1 = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
        sibling1 = list(sibling1.children)[0]
        sibling2 = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
        sibling2 = list(sibling2.children)[0]

        p = Parser()
        self.assertFalse(p._is_span_child(sibling1, sibling2))
        self.assertFalse(p._is_span_child(sibling2, sibling1))

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
        self.assertTrue(p._is_span_child(child, parent))
        self.assertFalse(p._is_span_child(parent, child))

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
        self.assertFalse(p._is_span_child(sibling1, sibling2))
        self.assertFalse(p._is_span_child(sibling2, sibling1))

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
        self.assertTrue(p._is_span_child(child, parent))
        self.assertFalse(p._is_span_child(parent, child))

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
        self.assertFalse(p._is_span_child(sibling1, sibling2))
        self.assertFalse(p._is_span_child(sibling2, sibling1))

    def test_is_child_relative_text_is_not_child(self):
        sibling1 = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">iPad</span>""",
            features="html.parser",
        )
        sibling1 = list(sibling1.children)[0]
        sibling2 = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:6.5pt;font-weight:400;line-height:120%;position:relative;top:-3.5pt;vertical-align:baseline">Â®</span>""",
            features="html.parser",
        )
        sibling2 = list(sibling2.children)[0]

        p = Parser()
        self.assertFalse(p._is_span_child(sibling1, sibling2))
        self.assertFalse(p._is_span_child(sibling2, sibling1))

    def test_is_child_descending_priority_order(self):
        child = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Unless otherwise stated.</span>""",
            features="html.parser",
        )
        child = list(child.children)[0]
        parent = BeautifulSoup(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span>""",
            features="html.parser",
        )
        parent = list(parent.children)[0]
        p = Parser()
        self.assertTrue(p._is_span_child(child, parent))
        self.assertFalse(p._is_span_child(parent, child))

    def test_is_div_child(self):
        child = BeautifulSoup(
            """<div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>""",
            features="html.parser",
        )
        child = list(child.children)[0]
        parent = BeautifulSoup(
            """<div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1.Â&nbsp;Â&nbsp;Â&nbsp;Â&nbsp;Business</span></div>""",
            features="html.parser",
        )
        parent = list(parent.children)[0]

        p = Parser()
        self.assertTrue(p._is_div_child(child, parent))
        self.assertFalse(p._is_div_child(parent, child))

    def test_walk_soup(self):
        soup = BeautifulSoup(
            """<body>
<div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
<div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
<div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1.;Business</span></div>
<div style="margin-top:6pt;text-align:justify"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%"><tbody><tr><td style="width:1.0%"></td><td style="width:59.280%"></td><td style="width:0.1%"></td><td style="width:1.0%"></td><td style="width:11.619%"></td><td style="width:0.1%"></td><td style="width:0.1%"></td><td style="width:0.530%"></td><td style="width:0.1%"></td><td style="width:1.0%"></td><td style="width:11.619%"></td><td style="width:0.1%"></td><td style="width:0.1%"></td><td style="width:0.530%"></td><td style="width:0.1%"></td><td style="width:1.0%"></td><td style="width:11.622%"></td><td style="width:0.1%"></td></tr><tr><td colspan="3" style="padding:0 1pt"></td><td colspan="3" style="padding:2px 1pt;text-align:center;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:8pt;font-weight:700;line-height:100%">2020</span></td><td colspan="3" style="padding:0 1pt"></td><td colspan="3" style="padding:2px 1pt;text-align:center;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:8pt;font-weight:700;line-height:100%">2019</span></td><td colspan="3" style="padding:0 1pt"></td><td colspan="3" style="padding:2px 1pt;text-align:center;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:8pt;font-weight:700;line-height:100%">2018</span></td></tr><tr><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Cash, cash equivalents and marketable securities </span><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:5.85pt;font-weight:400;line-height:100%;position:relative;top:-3.15pt;vertical-align:baseline">(1)</span></div></td><td style="border-top:1pt solid #000000;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="border-top:1pt solid #000000;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">191,830Â&nbsp;</span></td><td style="border-top:1pt solid #000000;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="padding:0 1pt"></td><td style="border-top:1pt solid #000000;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="border-top:1pt solid #000000;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">205,898Â&nbsp;</span></td><td style="border-top:1pt solid #000000;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="padding:0 1pt"></td><td style="border-top:1pt solid #000000;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="border-top:1pt solid #000000;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">237,100Â&nbsp;</span></td><td style="border-top:1pt solid #000000;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Property, plant and equipment, net</span></div></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">36,766Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">37,378Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">41,304Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Commercial paper</span></div></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">4,996Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#ffffff;padding:0 1pt"></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">5,980Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#ffffff;padding:0 1pt"></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">11,964Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Total term debt</span></div></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">107,440Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">102,067Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">102,519Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="background-color:#ffffff;padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Working capital</span></div></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">38,321Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#ffffff;padding:0 1pt"></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">57,101Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#ffffff;padding:0 1pt"></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">15,410Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Cash generated by operating activities</span></div></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">80,674Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">69,391Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">77,434Â&nbsp;</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="background-color:#ffffff;padding:2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Cash generated by/(used in) investing activities</span></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">(4,289)</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#ffffff;padding:0 1pt"></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">45,896Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#ffffff;padding:0 1pt"></td><td style="background-color:#ffffff;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#ffffff;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">16,066Â&nbsp;</span></td><td style="background-color:#ffffff;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:top"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">Cash used in financing activities</span></div></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">(86,820)</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">(90,976)</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td><td colspan="3" style="background-color:#efefef;padding:0 1pt"></td><td style="background-color:#efefef;padding:2px 0 2px 1pt;text-align:left;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">$</span></td><td style="background-color:#efefef;padding:2px 0;text-align:right;vertical-align:bottom"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%">(87,876)</span></td><td style="background-color:#efefef;padding:2px 1pt 2px 0;text-align:right;vertical-align:bottom"></td></tr></tbody></table></div>
                </body>""",
            features="html.parser",
        )

        p = Parser()
        walker = p._walk_soup(soup, not_into=["table", "span"])
        self.assertEqual(next(walker).name, "body")
        self.assertEqual(next(walker).name, "div")
        self.assertEqual(next(walker).name, "span")
        self.assertEqual(next(walker).name, "div")
        self.assertEqual(next(walker).name, "div")
        self.assertEqual(next(walker).name, "span")
        self.assertEqual(next(walker).name, "div")
        self.assertEqual(next(walker).name, "table")
        self.assertRaises(StopIteration, next, walker)

    def test_get_hierarchy(self):
        soup = BeautifulSoup(
            """<body>
            <div style="margin-top:16pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
            <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company designs</span></div>
            <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">good products</span></div>
                </body>""",
            features="html.parser",
        )
        soup_hierarchy = {
            "root": [{"Products": ["The Company designs", "good products"]}]
        }

        p = Parser()
        hierarchy = p.get_hierarchy(soup)
        self.assertDictEqual(hierarchy, soup_hierarchy)

    def test_get_hierarchy_div_child(self):
        soup = BeautifulSoup(
            """<body>
            <div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
                </body>""",
            features="html.parser",
        )

        expected_hierarchy = {
            "root": [{"Item 1. Business": ["Company Background", "Products"]}]
        }
        p = Parser()
        extracted_hierarchy = p.get_hierarchy(soup)
        self.assertDictEqual(extracted_hierarchy, expected_hierarchy)

    def test_get_hierarchy_div_child_but_not_span_child(self):
        soup = BeautifulSoup(
            """<body>
            <div style="margin-top:12pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Unless otherwise stated.</span></div>
            <div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
                </body>""",
            features="html.parser",
        )

        expected_hierarchy = {"root": ["Unless otherwise stated.", "PART I"]}
        p = Parser()
        extracted_hierarchy = p.get_hierarchy(soup)
        self.assertDictEqual(extracted_hierarchy, expected_hierarchy)

    def test_get_hierarchy_large(self):
        soup = BeautifulSoup(
            """<body>
            <div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
            <div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
            <div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
            <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company is a California corporation established in 1977.</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Mac</span></div>
                </body>""",
            features="html.parser",
        )
        soup_hierarchy = {
            "root": [
                {
                    "PART I": [
                        {
                            "Item 1. Business": [
                                {
                                    "Company Background": [
                                        "The Company is a California corporation established in 1977."
                                    ]
                                },
                                {"Products": ["iPhone", "Mac"]},
                            ]
                        }
                    ]
                }
            ]
        }

        p = Parser()
        extracted_hierarchy = p.get_hierarchy(soup)
        self.maxDiff = None
        self.assertDictEqual(extracted_hierarchy, soup_hierarchy)

    def test_hierarchy_to_string(self):
        soup = BeautifulSoup(
            """<body>
            <div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
            <div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
            <div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
            <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company is a California corporation established in 1977.</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span></div>
            <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Mac</span></div>
                </body>""",
            features="html.parser",
        )
        soup_hierarchy = {
            "root": [
                {
                    "PART I": [
                        {
                            "Item 1. Business": [
                                {
                                    "Company Background": [
                                        "The Company is a California corporation established in 1977."
                                    ]
                                },
                                {"Products": ["iPhone", "Mac"]},
                            ]
                        }
                    ]
                }
            ]
        }
        soup_hierarchy_string = """
root
\tPART I
\t\tItem 1. Business
\t\t\tCompany Background
\t\t\t\tThe Company is a California corporation established in 1977.
\t\t\tProducts
\t\t\t\tiPhone
\t\t\t\tMac
"""

        p = Parser()
        extracted_hierarchy = p.get_hierarchy(soup)
        self.maxDiff = None
        self.assertDictEqual(extracted_hierarchy, soup_hierarchy)
