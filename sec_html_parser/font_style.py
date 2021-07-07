from dataclasses import dataclass
from typing import Optional, Tuple, Union

import regex as re
from bs4.element import Tag


@dataclass
class FontStyle:
    """Parsed HTML span style element attributes"""

    size: Optional[int]
    weight: Optional[int]
    style: Optional[str]

    def __init__(self, node_or_style: Union[str, Tag]) -> None:
        _font_size_re = re.compile("font-size:(\d+)")
        _font_weight_re = re.compile("font-weight:(\d+)")
        _font_style_re = re.compile("font-style:([a-zA-Z]+)")

        span_style = self._get_style_string(node_or_style)

        size = _font_size_re.search(span_style)
        self.size = None if size is None else int(size.group(1))

        weight = _font_weight_re.search(span_style)
        self.weight = None if weight is None else int(weight.group(1))

        style = _font_style_re.search(span_style)
        self.style = None if style is None else style.group(1)

    @staticmethod
    def _get_style_string(node_or_style: Union[str, Tag]) -> str:
        """Get a style string from a string or a bs4 Node"""

        if isinstance(node_or_style, str):
            return node_or_style
        elif isinstance(node_or_style, Tag):
            node_style = node_or_style.get("style")
            if node_style is not None:
                return node_style
            else:
                raise ValueError("Given node didn't have a 'style' attribute")
        else:
            raise ValueError(
                "Can't create FontStyle from object"
                f"of type '{node_or_style.__class__.__name__}'"
            )
