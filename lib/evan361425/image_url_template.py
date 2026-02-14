"""
Main plugin module for ImageUrlTemplate
Transforms relative image URLs to absolute URLs with domain and blog location
Example: src/essay/my-essay.md with ![](image.png) becomes ![](${domain}/essay/my-essay/image.png)
"""

import re

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from .util import info

# Regular expressions for markdown image syntax
# Matches: ![alt text](url) or ![](url)
IMAGE_PATTERN = r"!\[([^\]]*)\]\(([^)]+)\)"


class MarkdownImageUrlTemplatePlugin(BasePlugin):
    """
    Plugin to transform relative image URLs in markdown files.
    """

    config_scheme = (("domain", config_options.Type(str, default="")),)

    domain: str

    def __init__(self) -> None:
        self._image_count = 0
        super().__init__()

    # ----------------
    # Properties
    # ----------------
    @property
    def total_count(self):
        """Total images transformed"""
        return self._image_count

    # ----------------
    # Event handlers
    # ----------------
    def on_config(self, config):
        """
        Initialize plugin with configuration
        """
        self.domain = self.config["domain"]
        if not self.domain:
            self.domain = config["site_url"]
        return config

    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        dir_path = page.file.src_path.rsplit(".", 1)[0]

        if page.meta.get("hasCover") is True and not page.meta.get("image"):
            page.meta["image"] = f"{self.domain}/{dir_path}/_page.avif"
        if page.meta.get("image") and not page.meta["image"].startswith("https://"):
            path = (
                page.meta["image"]
                if page.meta["image"].startswith("/")
                else f"/{dir_path}/{page.meta['image']}"
            )
            page.meta["image"] = f"{self.domain}{path}"

        def replace_url(match: re.Match[str]) -> str:
            alt_text = match.group(1)
            url = match.group(2)

            # Skip if URL is already absolute (starts with http://, https://)
            if url.startswith(("http://", "https://")):
                return match.group(0)

            path = f"{dir_path}/{url}"
            if url.startswith("/"):
                path = url

            # Transform relative URL to include domain and directory
            transformed_url = f"{self.domain}/{path}.avif"
            self._image_count += 1

            return f"![{alt_text}]({transformed_url})"

        return re.sub(IMAGE_PATTERN, replace_url, markdown)

    def on_post_build(self, **_kwargs):
        """Log total count after build"""
        info(f"Transformed {self.total_count} image URLs")
