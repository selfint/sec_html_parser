import bs4.element
from bs4 import BeautifulSoup

from sec_html_parser.font_style import FontStyle


class Parser:
    def _is_child(self, node: bs4.element.Tag, other: bs4.element.Tag) -> bool:
        """Check if node is a child of other with respect to font styles"""

        # check that other has a style
        try:
            ostyle = FontStyle(other)
        except ValueError:
            return False

        # a node with no style is always a child
        try:
            nstyle = FontStyle(node)
        except ValueError:
            return True

        # check if style by size
        if ostyle.size is not None:
            if nstyle.size is not None and nstyle.size < ostyle.size:
                return True

        # check if style by weight
        if ostyle.weight is not None:
            if nstyle.weight is not None and nstyle.weight < ostyle.weight:
                return True

        # child if style by style
        if ostyle.style is not None:
            if nstyle.style is not None:
                if ostyle.style == "italic" and nstyle.style != "italic":
                    return True
            return ostyle.style == "italic"

        # if not child by any of the above then it is not a child
        return False
