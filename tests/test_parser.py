import pytest
from bs4 import BeautifulSoup

from sec_html_parser.parser import Parser


def test_is_child_size_larger():
    child = BeautifulSoup('<span style="font-size:9pt"/>', features="html.parser")
    child = list(child.children)[0]
    parent = BeautifulSoup('<span style="font-size:10pt"/>', features="html.parser")
    parent = list(parent.children)[0]

    p = Parser()
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_child_size_equal():
    sibling1 = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
    sibling1 = list(sibling1.children)[0]
    sibling2 = BeautifulSoup('<span style="font-size:10pt"', features="html.parser")
    sibling2 = list(sibling2.children)[0]

    p = Parser()
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_size_equal_weight_larger():
    child = BeautifulSoup(
        '<span style="font-size:10pt;font-weight:400"', features="html.parser"
    )
    child = list(child.children)[0]
    parent = BeautifulSoup(
        '<span style="font-size:10pt;font-weight:700"', features="html.parser"
    )
    parent = list(parent.children)[0]

    p = Parser()
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_child_size_equal_weight_equal():
    sibling1 = BeautifulSoup(
        '<span style="font-size:10pt;font-weight:400"', features="html.parser"
    )
    sibling1 = list(sibling1.children)[0]
    sibling2 = BeautifulSoup(
        '<span style="font-size:10pt;font-weight:400"', features="html.parser"
    )
    sibling2 = list(sibling2.children)[0]

    p = Parser()
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_size_equal_weight_equal_style_italic():
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
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_child_size_equal_weight_equal_style_equal():
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
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_relative_text_is_not_child():
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
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_descending_priority_order():
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
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_div_child():
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
    assert p._is_div_child(child, parent)
    assert not p._is_div_child(parent, child)


def test_walk_soup():
    soup = BeautifulSoup(
        """<body>
<div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
<div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
<div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1.;Business</span></div>
<div style="margin-top:6pt;text-align:justify"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%">snipped for test</table></div>
            </body>""",
        features="html.parser",
    )

    p = Parser()
    walker = p._walk_soup(soup, not_into=["table", "span"])
    assert next(walker).name == "body"
    assert next(walker).name == "div"
    assert next(walker).name == "span"
    assert next(walker).name == "div"
    assert next(walker).name == "div"
    assert next(walker).name == "span"
    assert next(walker).name == "div"
    assert next(walker).name == "table"
    with pytest.raises(StopIteration):
        next(walker)


def test_get_hierarchy():
    soup = BeautifulSoup(
        """<body>
        <div style="margin-top:16pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
        <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company designs</span></div>
        <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">good products</span></div>
            </body>""",
        features="html.parser",
    )
    soup_hierarchy = {"root": [{"Products": ["The Company designs", "good products"]}]}

    p = Parser()
    hierarchy = p.get_hierarchy(soup)
    assert hierarchy == soup_hierarchy


def test_get_hierarchy_div_child():
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
    assert extracted_hierarchy == expected_hierarchy


def test_get_hierarchy_div_child_but_not_span_child():
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
    assert extracted_hierarchy == expected_hierarchy


def test_get_hierarchy_large():
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
    assert extracted_hierarchy == soup_hierarchy


def test_hierarchy_to_string():
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
    soup_hierarchy_string = """root
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
    extracted_hierarchy_string = p.hierarchy_to_string(extracted_hierarchy)
    assert extracted_hierarchy_string == soup_hierarchy_string


def test_hierarchy_with_table():
    soup = BeautifulSoup(
        """<body>
<div style="margin-top:6pt;text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">TABLE OF CONTENTS</span></div>
<div style="margin-top:6pt;text-align:justify"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%"><tbody><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1.</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Business</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">1</a></span></div></td></tr><tr><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1A.</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Risk Factors</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">5</a></span></div></td></tr></tbody></table></div>
            </body>""",
        features="html.parser",
    )

    expected_hierarchy = {
        "root": [
            {
                "TABLE OF CONTENTS": [
                    {
                        "table": [
                            """<table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%"><tbody><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1.</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Business</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">1</a></span></div></td></tr><tr><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1A.</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Risk Factors</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">5</a></span></div></td></tr></tbody></table>"""
                        ]
                    }
                ]
            }
        ]
    }

    p = Parser()
    extracted_hierarchy = p.get_hierarchy(soup)

    assert extracted_hierarchy == expected_hierarchy
