from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Union

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

from sec_html_parser.div_style import DivStyle
from sec_html_parser.font_style import FontStyle


class Parser:
    def _is_span_child(self, node: Tag, other: Tag) -> bool:
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

        # text in relative position (top or bottom) is never a child
        # and can never have children
        if nstyle.relative or ostyle.relative:
            return False

        # check if style by size
        if ostyle.size is not None:
            if nstyle.size is not None:
                if nstyle.size < ostyle.size:
                    return True
                elif nstyle.size > ostyle.size:
                    return False

        # check if style by weight
        if ostyle.weight is not None:
            if nstyle.weight is not None:
                if nstyle.weight < ostyle.weight:
                    return True
                elif nstyle.weight > ostyle.weight:
                    return False

        # child if style by style
        if ostyle.style is not None:
            if nstyle.style is not None:
                if ostyle.style == "italic" and nstyle.style != "italic":
                    return True
                else:
                    return False
            return ostyle.style == "italic"

        # if not child by any of the above then it is not a child
        return False

    def _walk_soup(
        self,
        element: Union[BeautifulSoup, PageElement],
        not_into: List[str] = list(),
    ) -> Iterator[PageElement]:
        """
        Iterate given element and all its children in a depth-first manner

        Will not yield elements without a `name` (e.g. a text element in a span),
        neither will it yield elements whose `name` is in the `not_into` list.

        If given a `BeautifulSoup` object, only the children will be yielded
        (and recursed into if appropriate), not the `BeautifulSoup` object itself.
        """

        element_is_not_soup = not isinstance(element, BeautifulSoup)
        element_has_name = element.name is not None

        if element_is_not_soup and element_has_name:
            yield element

        element_has_children = hasattr(element, "children")
        if element_has_children:

            should_recurse = element.name not in not_into
            if should_recurse:
                for child in element.children:
                    yield from self._walk_soup(child, not_into)

    def get_file_hierarchy(self, path: Path, keep_nodes: bool = False) -> dict:
        """
        Get text hierarchy of text in a file, with respect to the style attribute
        of the elements in the soup.
        """

        soup = BeautifulSoup(path.read_text(), features="html.parser")

        return self.get_hierarchy(soup, keep_nodes)

    def get_hierarchy(self, soup: BeautifulSoup, keep_nodes: bool = False) -> dict:
        """
        Get text hierarchy of text in soup, with respect to the style attribute
        of the elements in the soup.
        """

        hierarchy = {"root": []}
        span_stack = []
        element_div = None
        for element_node in self._walk_soup(soup, not_into=["span", "table"]):
            if element_node.name == "div":
                element_div = element_node
            elif element_node.name == "span":
                element_content = element_node.text.strip()
                element_children = {element_content: []}
                element = (element_div, element_node, element_children[element_content])

                # pop elements from the stack until a parent is found
                for parent_div, parent_node, parent_children in reversed(span_stack):
                    div_child = (
                        True
                        if parent_div is None
                        else self._is_div_child(element_div, parent_div)
                    )
                    span_child = self._is_span_child(element_node, parent_node)
                    if (div_child and not span_child) or span_child:

                        # add the element as a child of the parent
                        parent_children.append(element_children)

                        # add a pointer to the element's children to the stack
                        span_stack.append(element)
                        break
                    else:
                        span_stack.pop()
                else:

                    # if no parent was found add the element as a child
                    # of the root node
                    hierarchy["root"].append(element_children)
                    span_stack.append(element)

        hierarchy = self._clean_leaves(hierarchy)

        return hierarchy

    def _clean_leaves(self, hierarchy: dict) -> dict:
        """Convert leaf nodes to strings instead of dictionaries with an empty list"""

        # first we get the name of the node
        name = list(hierarchy)[0]

        # then we check if it is a leaf
        if len(hierarchy[name]) == 0:

            # if so then we return the name of the node
            return name
        else:

            # if not then we clean all the child nodes of the current node
            return {name: [self._clean_leaves(child) for child in hierarchy[name]]}

    def _is_div_child(self, node: Tag, other: Tag) -> bool:
        """Check if node is a child of other with respect to div styles"""

        # check that other has a style
        try:
            ostyle = DivStyle(other)
        except ValueError:
            return False

        # a div with no style is always a child
        try:
            nstyle = DivStyle(node)
        except ValueError:
            return True

        # check if div has a smaller margin than other
        if ostyle.margin_top is not None:
            if nstyle.margin_top is not None:
                if nstyle.margin_top < ostyle.margin_top:
                    return True

        return False

    def hierarchy_to_string(self, hierarchy: dict, depth: int = 0) -> str:
        """Get a string representation of a hierarchy"""

        if isinstance(hierarchy, str):
            return "\t" * depth + hierarchy + "\n"

        key = list(hierarchy.keys())[0]
        string = "\t" * depth + key + "\n"
        for child in hierarchy[key]:
            string += self.hierarchy_to_string(child, depth + 1)

        return string
