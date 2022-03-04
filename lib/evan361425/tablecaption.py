"""
Main plugin module for tablecaption
"""

from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

from .util import info


# ------------------------
# Constants and utilities
# ------------------------
DELIMITER = "~"

# ------------------------
# Plugin
# ------------------------
class MarkdownTablecaptionPlugin(BasePlugin):
    """
    Plugin for interpreting Mermaid code
    """

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
            header = table.select_one("th")
            if not header:
                continue
            origin = header.getText().split(DELIMITER, 1)
            if len(origin) == 1 or not origin[0]:
                continue
            title, text = origin
            caption = soup.new_tag("caption")
            caption.string = title

            header.string = text
            header.findParent("table").insert(0, caption)

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
