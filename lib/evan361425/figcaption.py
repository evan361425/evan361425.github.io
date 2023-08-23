"""
Main plugin module for FigCaption
"""

from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

from .util import info


# ------------------------
# Constants and utilities
# ------------------------
IGNORE_PREFIX = "!"
IGNORE_FIRST_CHAR = "/"


# ------------------------
# Plugin
# ------------------------
class MarkdownFigcaptionPlugin(BasePlugin):
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
    def on_post_page(self, output_content, **_kwargs):
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

            quote = image.parent.next_sibling
            if quote and str(quote) == "\n":
                quote = quote.next_sibling

            figure = soup.new_tag("figure")
            figcaption = soup.new_tag("figcaption")
            caption = image.attrs["alt"]

            if quote and quote.name == "blockquote":
                quoted = quote.findChild("p").encode_contents().decode("utf-8")
                if quoted.startswith(IGNORE_FIRST_CHAR):
                    new_html = str(quote).replace(IGNORE_FIRST_CHAR, "", 1)
                    new_ele = BeautifulSoup(new_html, "html.parser")
                    quote.insert_after(new_ele)
                    quote.decompose()
                else:
                    if quoted.startswith("{"):
                        index = quoted.index("}")
                        width, height = quoted[1:index].split("x")
                        image.attrs["width"] = width
                        image.attrs["height"] = height
                        quoted = quoted[index + 1 :]
                    caption = caption + "<br/>來源於：" + quoted.strip()
                    quote.extract()

            figcaption.append(BeautifulSoup(caption, "html.parser"))

            # replace image to figure:
            image.replaceWith(figure)
            # Append inside figure
            figure.append(image)
            figure.append(figcaption)
            self.__increment()

        return str(soup)

    def on_post_build(self, **_kwargs):
        """
        Log total count after built
        """

        info(f"Found {self.total_count} images")

    # ------------------------
    # Private
    # ------------------------
    def __init__(self) -> None:
        self._fig_count = 0
        super().__init__()

    def __increment(self, count=1):
        """
        Record total count for logging
        """
        self._fig_count += count
