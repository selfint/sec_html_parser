import pytest
from bs4 import BeautifulSoup, Tag

from sec_html_parser.parser import Parser


def _node(text: str) -> Tag:
    """Convert text to a Tag represented by the given text"""
    return list(BeautifulSoup(text, features="html.parser").children)[0]


def test_is_child_size_larger():
    child = _node('<span style="font-size:9pt"/>')
    parent = _node('<span style="font-size:10pt"/>')

    p = Parser()
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_child_size_equal():
    sibling1 = _node('<span style="font-size:10pt"/>')
    sibling2 = _node('<span style="font-size:10pt"/>')

    p = Parser()
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_size_equal_weight_larger():
    child = _node('<span style="font-size:10pt;font-weight:400"')
    parent = _node('<span style="font-size:10pt;font-weight:700"')

    p = Parser()
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_child_size_equal_weight_equal():
    sibling1 = _node('<span style="font-size:10pt;font-weight:400"')
    sibling2 = _node('<span style="font-size:10pt;font-weight:400"')

    p = Parser()
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_size_equal_weight_equal_style_italic():
    child = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">iPhone</span>"""
    )
    parent = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>"""
    )

    p = Parser()
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_child_size_equal_weight_equal_style_equal():
    sibling1 = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>"""
    )
    sibling2 = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>"""
    )

    p = Parser()
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_relative_text_is_not_child():
    sibling1 = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">iPad</span>"""
    )
    sibling2 = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:6.5pt;font-weight:400;line-height:120%;position:relative;top:-3.5pt;vertical-align:baseline">Â®</span>"""
    )

    p = Parser()
    assert not p._is_span_child(sibling1, sibling2)
    assert not p._is_span_child(sibling2, sibling1)


def test_is_child_descending_priority_order():
    child = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Unless otherwise stated.</span>"""
    )
    parent = _node(
        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span>"""
    )
    p = Parser()
    assert p._is_span_child(child, parent)
    assert not p._is_span_child(parent, child)


def test_is_div_child():
    child = _node(
        """<div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>"""
    )
    parent = _node(
        """<div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1.Â&nbsp;Â&nbsp;Â&nbsp;Â&nbsp;Business</span></div>"""
    )

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
    soup_hierarchy = {
        "root": [
            {
                _node(
                    """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span>"""
                ): [
                    _node(
                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company designs</span>"""
                    ),
                    _node(
                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">good products</span>"""
                    ),
                ]
            }
        ]
    }

    p = Parser()
    hierarchy = p.get_soup_hierarchy(soup)
    assert hierarchy == soup_hierarchy


def test_get_hierarchy_div_child():
    soup = _node(
        """<body>
        <div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
            </body>"""
    )
    expected_hierarchy = {
        "root": [
            {
                _node(
                    """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span>"""
                ): [
                    _node(
                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span>"""
                    ),
                    _node(
                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span>"""
                    ),
                ]
            }
        ]
    }
    p = Parser()
    extracted_hierarchy = p.get_soup_hierarchy(soup)
    assert extracted_hierarchy == expected_hierarchy


def test_get_hierarchy_div_child_but_not_span_child():
    soup = _node(
        """<body>
        <div style="margin-top:12pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Unless otherwise stated.</span></div>
        <div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
            </body>"""
    )
    expected_hierarchy = {
        "root": [
            _node(
                """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Unless otherwise stated.</span>"""
            ),
            _node(
                """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span>"""
            ),
        ]
    }
    p = Parser()
    extracted_hierarchy = p.get_soup_hierarchy(soup)
    assert extracted_hierarchy == expected_hierarchy


def test_get_hierarchy_large():
    soup = _node(
        """<body>
        <div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
        <div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
        <div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
        <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company is a California corporation established in 1977.</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Mac</span></div>
            </body>"""
    )
    soup_hierarchy = {
        "root": [
            {
                _node(
                    """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span>"""
                ): [
                    {
                        _node(
                            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span>"""
                        ): [
                            {
                                _node(
                                    """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span>"""
                                ): [
                                    _node(
                                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company is a California corporation established in 1977.</span>"""
                                    )
                                ]
                            },
                            {
                                _node(
                                    """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span>"""
                                ): [
                                    _node(
                                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span>"""
                                    ),
                                    _node(
                                        """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Mac</span>"""
                                    ),
                                ]
                            },
                        ]
                    }
                ]
            }
        ]
    }

    p = Parser()
    extracted_hierarchy = p.get_soup_hierarchy(soup)
    assert extracted_hierarchy == soup_hierarchy


def test_hierarchy_with_table():
    source = """<body>
<div style="margin-top:6pt;text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">TABLE OF CONTENTS</span></div>
<div style="margin-top:6pt;text-align:justify"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%"><tbody><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1.</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Business</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">1</a></span></div></td></tr><tr><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1A.</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Risk Factors</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">5</a></span></div></td></tr></tbody></table></div>
            </body>"""
    expected_hierarchy = {
        "root": [
            {
                _node(
                    """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">TABLE OF CONTENTS</span>"""
                ): [
                    _node(
                        """<table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%"><tbody><tr><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1.</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Business</a></span></div></td><td colspan="3" style="background-color:#efefef;padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_13" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">1</a></span></div></td></tr><tr><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Item 1A.</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="padding-left:9pt;text-indent:-9pt"><span style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#0000ff;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:underline">Risk Factors</a></span></div></td><td colspan="3" style="padding:2px 1pt;text-align:left;vertical-align:bottom"><div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%"><a href="#ief781ab58e4f4fcaa872ddbd30da40e1_16" style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:100%;text-decoration:none">5</a></span></div></td></tr></tbody></table>"""
                    )
                ]
            }
        ]
    }

    p = Parser()
    extracted_hierarchy = p.get_hierarchy(source)

    assert extracted_hierarchy == expected_hierarchy


def test_get_hierarchy_empty_table_is_ignored():
    source = """<body>
<div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:11pt;font-weight:700;line-height:120%">Washington, D.C. 20549</span></div>
<div style="margin-top:6pt;text-align:center"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:19.444%"><tbody><tr><td style="width:1.0%"></td><td style="width:98.900%"></td><td style="width:0.1%"></td></tr><tr style="height:3pt"><td colspan="3" style="border-bottom:1pt solid #000000;padding:0 1pt"></td></tr></tbody></table></div>
            </body>"""

    expected_hierarchy = {
        "root": [
            _node(
                """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:11pt;font-weight:700;line-height:120%">Washington, D.C. 20549</span>"""
            )
        ]
    }
    p = Parser()
    extracted_hierarchy = p.get_hierarchy(source)
    assert extracted_hierarchy == expected_hierarchy


def test_get_hierarchy_from_string():
    string = """<body>
<div style="text-align:center"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:11pt;font-weight:700;line-height:120%">Washington, D.C. 20549</span></div>
<div style="margin-top:6pt;text-align:center"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:19.444%"><tbody><tr><td style="width:1.0%"></td><td style="width:98.900%"></td><td style="width:0.1%"></td></tr><tr style="height:3pt"><td colspan="3" style="border-bottom:1pt solid #000000;padding:0 1pt"></td></tr></tbody></table></div>
            </body>"""
    soup = _node(string)

    p = Parser()
    expected_hierarchy = p.get_soup_hierarchy(soup)
    extracted_hierarchy = p.get_string_hierarchy(string)
    assert extracted_hierarchy == expected_hierarchy


def test_unsupported_type_raises_type_error():
    p = Parser()
    with pytest.raises(TypeError):
        p.get_hierarchy(["unsupported type"])


def test_walk_hierarchy():
    target = """<body>
<div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
<div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
<div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1.;Business</span></div>
<div style="margin-top:6pt;text-align:justify"><table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%">snipped for test</table></div>
</body>"""

    p = Parser()
    hierarchy = p.get_hierarchy(target)
    walker = p._walk_hierarchy_nodes(hierarchy)
    assert next(walker) == (
        False,
        1,
        _node(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span>"""
        ),
    )
    assert next(walker) == (
        False,
        2,
        _node(
            """<span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1.;Business</span>"""
        ),
    )
    assert next(walker) == (
        True,
        3,
        _node(
            """<table style="border-collapse:collapse;display:inline-table;vertical-align:top;width:100.000%">snipped for test</table>"""
        ),
    )
    with pytest.raises(StopIteration):
        next(walker)


def test_get_hierarchy_html():
    source = """<body>
        <div style="margin-top:18pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></div>
        <div id="ief781ab58e4f4fcaa872ddbd30da40e1_13"></div>
        <div style="margin-top:12pt;padding-left:45pt;text-align:justify;text-indent:-45pt"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></div>
        <div style="margin-top:6pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company is a California corporation established in 1977.</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span></div>
        <div style="margin-top:9pt;text-align:justify"><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Mac</span></div>
            </body>"""
    # soup_hierarchy = {
    # "root": [
    # {
    # "PART I": [
    # {
    # "Item 1. Business": [
    # {
    # "Company Background": [
    # "The Company is a California corporation established in 1977."
    # ]
    # },
    # {"Products": ["iPhone", "Mac"]},
    # ]
    # }
    # ]
    # }
    # ]
    # }
    expected_html = """<html>
<h1><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">PART I</span></h1>
<h2><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Item 1. Business</span></h2>
<h3><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Company Background</span></h3>
<p><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:400;line-height:120%">The Company is a California corporation established in 1977.</span></p>
<h3><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-weight:700;line-height:120%">Products</span></h3>
<p><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">iPhone</span></p>
<p><span style="color:#000000;font-family:'Helvetica',sans-serif;font-size:9pt;font-style:italic;font-weight:400;line-height:120%">Mac</span></p>
</html>"""
    expected_html = BeautifulSoup(expected_html, features="html.parser").prettify()

    p = Parser()
    extracted_html = p.get_hierarchy_html(source)

    assert extracted_html == expected_html
