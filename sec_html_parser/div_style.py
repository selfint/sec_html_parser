from dataclasses import dataclass
from typing import Optional, Union

import regex as re
from bs4.element import Tag

from sec_html_parser.span_style import SpanStyle


@dataclass
class DivStyle:
    """Parsed HTML div style element attributes"""

    margin_top: Optional[float]

    def __init__(self, node_or_style: Union[str, Tag]) -> None:
        _margin_top_re = re.compile("margin-top:(\d+\.?\d*)pt;?")

        div_style_str = SpanStyle._get_style_string(node_or_style)

        size = _margin_top_re.search(div_style_str)
        self.margin_top = None if size is None else float(size.group(1))
