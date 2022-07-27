"""
Main plugin module for TableCaption
"""

from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

from .util import info


# ------------------------
# Constants and utilities
# ------------------------
IGNORE_FIRST_CHAR = "/"

# ------------------------
# Plugin
# ------------------------
class MarkdownTablecaptionPlugin(BasePlugin):
    config_scheme = ()

    # ------------------------
    # Properties
    # Do not call them before on_config was run!
    # ------------------------
    @property
    def total_count(self):
        """
        Total diagrams founded
        """
        return self._table_count

    # ------------------------
    # Event handlers
    # ------------------------
    def on_config(self, config):
        """
        The initial configuration
        store the configuration in properties
        """
        self.__initialize(config=config)

    def on_post_page(self, output_content, config, page, **kwargs):
        """
        Actions for each page:
        generate the HTML code for all code items marked as 'img'
        """
        if "<table>" not in output_content:
            # Skip unecessary HTML parsing
            return output_content

        soup = BeautifulSoup(output_content, "html.parser")
        for table in soup.select("table"):
            # first next must be newline
            quote = table.next_sibling
            if str(quote) == "\n":
                quote = quote.next_sibling
            if quote.name != "blockquote":
                continue

            title = quote.getText().strip()
            if len(title) == 0:
                continue

            if title.startswith(IGNORE_FIRST_CHAR):
                new_html = str(quote).replace("/", "", 1)
                new_ele = BeautifulSoup(new_html, "html.parser")
                quote.insert_after(new_ele)
                quote.decompose()
                continue

            caption = soup.new_tag("caption")
            caption.string = title
            table.insert(0, caption)
            quote.decompose()

            self.__increment()

        return str(soup)

    def on_post_build(self, config):
        """
        Log total count after built
        """

        info("Found %s table" % self.total_count)

    # ------------------------
    # Private
    # ------------------------
    def __initialize(self, config):
        self._table_count = 0

    def __increment(self, count=1):
        """
        Record total count for logging
        """
        self._table_count += count
