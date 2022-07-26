"""
Main plugin module for figcaption
"""

from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

from .util import info


# ------------------------
# Constants and utilities
# ------------------------
IGNORE_PREFIX = "!"

# ------------------------
# Plugin
# ------------------------
class MarkdownFigcaptionPlugin(BasePlugin):
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
        if "<img " not in output_content:
            # Skip unecessary HTML parsing
            return output_content

        soup = BeautifulSoup(output_content, "html.parser")
        for image in soup.select("img", alt=True):
            if "alt" not in image.attrs or image.attrs["alt"] == "":
                continue
            if image.attrs["alt"].startswith(IGNORE_PREFIX):
                image.attrs["alt"] = image.attrs["alt"][2:]
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
