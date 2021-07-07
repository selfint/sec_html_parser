from dataclasses import dataclass
from typing import Optional, Tuple

import regex as re


@dataclass
class FontStyle:
    """Parsed HTML span style element attributes"""

    size: Optional[int]
    weight: Optional[int]
    style: Optional[str]

    def __init__(self, span_style: str) -> None:
        _font_size_re = re.compile("font-size:(\d+)")
        _font_weight_re = re.compile("font-weight:(\d+)")
        _font_style_re = re.compile("font-style:([a-zA-Z]+)")

        size = _font_size_re.search(span_style)
        self.size = None if size is None else int(size.group(1))

        weight = _font_weight_re.search(span_style)
        self.weight = None if weight is None else int(weight.group(1))

        style = _font_style_re.search(span_style)
        self.style = None if style is None else style.group(1)
