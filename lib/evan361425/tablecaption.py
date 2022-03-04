"""
Main plugin module for tablecaption
"""

from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

from .util import info


# ------------------------
# Constants and utilities
# ------------------------
DELIMITER = "!"

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
        return self._fig_count

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
        if "<table " not in output_content:
            # Skip unecessary HTML parsing
            return output_content

        soup = BeautifulSoup(output_content, "html.parser")
        for header in soup.select("table th:first-child"):
            table.tex
            if (
                "alt" not in table.attrs
                or image.attrs["alt"] == ""
                or image.attrs["alt"].startswith(IGNORE_PREFIX)
            ):
                continue
            figure = soup.new_tag("figure")
            figcaption = soup.new_tag("figcaption")
            figcaption.string = image.attrs["alt"]
            # replace image to figure:
            image.replaceWith(figure)
            # Append inside figure
            figure.append(image)
            figure.append(figcaption)
            self.__increment()

        return str(soup)

    def on_post_build(self, config):
        """
        Log total count after built
        """

        info("Found %s images" % self.total_count)

    # ------------------------
    # Private
    # ------------------------
    def __initialize(self, config):
        self._fig_count = 0

    def __increment(self, count=1):
        """
        Record total count for logging
        """
        self._fig_count += count
