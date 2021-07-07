from bs4 import BeautifulSoup


class Parser:
    def parse_html_str(self, text: str) -> dict:
        """Extract text hierarchy from unstructured HTML text"""
