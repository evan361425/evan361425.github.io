import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


class ClearNewlinePlugin(BasePlugin):
    def on_page_content(
        self, html: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str:
        r"""
        Use `find site -name '*' -type f | xargs ggrep -Pzo "[\x{4e00}-\x{9fa5}]\n[\x{4e00}-\x{9fa5}]"`
        to find all the Chinese characters with newlines in between, and then remove the newlines.
        """
        html = re.sub(r"([，。！？：；）」])\s*\n\s*", r"\1", html)
        html = re.sub(r"\n([（「])", r"\1", html)
        return html
