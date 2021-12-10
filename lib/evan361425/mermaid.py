"""
Main plugin module for mermaid
"""

from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType
from bs4 import BeautifulSoup

from . import pyjs
from .util import debug, info, libname, url_exists


# ------------------------
# Constants and utilities
# ------------------------
# the default (recommended) mermaid lib
MERMAID_LIB_VERSION = "8.8.0"
MERMAID_LIB = "https://unpkg.com/mermaid@%s/dist/mermaid.min.js"
# Two conditions for activating custom fences:
SUPERFENCES_EXTENSION = "pymdownx.superfences"
CUSTOM_FENCE_FN = "fence_mermaid_custom"

# ------------------------
# Plugin
# ------------------------
class MarkdownMermaidPlugin(BasePlugin):
    """
    Plugin for interpreting Mermaid code
    """

    config_scheme = (
        ("version", PluginType(str, default=MERMAID_LIB_VERSION)),
        (
            "arguments",
            PluginType(
                dict,
                default={
                    "theme": "^(JSON.parse(window.localStorage.getItem('/.__palette')).index == 1) ? 'dark' : 'light'"
                },
            ),
        ),
    )

    # ------------------------
    # Properties
    # Do not call them before on_config was run!
    # ------------------------
    @property
    def full_config(self):
        """
        The full plugin's configuration object,
        which also includes the contents of the yaml config file.
        """
        return self._full_config

    @property
    def mermaid_args(self):
        """
        The arguments for mermaid.
        """
        return self._mermaid_args

    @property
    def total_count(self):
        """
        Total diagrams founded
        """
        return self._mermaids_count

    @property
    def activate_custom_loader(self):
        """
        Predicate: activate the custom loader for superfences?
        The rule is to activate:
            1. superfences extension is activated
            2. it specifies 'fence_mermaid_custom' as
               as format function (instead of fence_mermaid)
        """
        return self._activate_custom_loader

    @property
    def extra_mermaid_lib(self):
        """
        Provides the mermaid library defined in mkdocs.yml (if any)
        """
        return self._extra_mermaid_lib

    @property
    def mermaid_lib(self):
        """
        Provides the actual mermaid library used
        """
        return self._mermaid_lib

    @property
    def js_content(self):
        return self._js_content

    # ------------------------
    # Event handlers
    # ------------------------
    def on_config(self, config):
        """
        The initial configuration
        store the configuration in properties
        """
        # here we use the standard self.config property:
        # (this can get confusing...)
        self._mermaid_args = self.config["arguments"]
        debug("Initialization arguments:", self.mermaid_args)

        self.__initialize(config=config)
        assert isinstance(self.mermaid_args, dict)

        if self.extra_mermaid_lib:
            info("Explicit mermaid library:\n  ", self.extra_mermaid_lib)
        else:
            info("Using mermaid library %s" % self.config["version"])

    def on_post_page(self, output_content, config, page, **kwargs):
        """
        Actions for each page:
        generate the HTML code for all code items marked as 'mermaid'
        """
        if "mermaid" not in output_content:
            # Skip unecessary HTML parsing
            return output_content
        soup = BeautifulSoup(output_content, "html.parser")
        page_name = page.title
        # first, determine if the page has diagrams:
        if self.activate_custom_loader:
            # the custom loader has its specific marking
            # <pre class = 'mermaid'><code> ... </code></pre>
            debug("Custom loader activated")
            mermaids = len(soup.select("pre.mermaid code"))
        else:
            # standard mermaid can accept two types of marking:
            # <pre><code class = 'mermaid'> ... </code></pre>
            # but since we want only <div> for best compatibility,
            # it needs to be replaced
            # NOTE: Python-Markdown changed its representation of code blocks
            # https://python-markdown.github.io/change_log/release-3.3/
            pre_code_tags = soup.select("pre code.mermaid") or soup.select(
                "pre code.language-mermaid"
            )
            no_found = len(pre_code_tags)
            if no_found:
                debug(
                    "Page '%s': found %s diagrams "
                    "(with <pre><code='[language-]mermaid'>), converting to <div>..."
                    % (page_name, len(pre_code_tags))
                )
                for tag in pre_code_tags:
                    content = tag.text
                    new_tag = soup.new_tag("div", attrs={"class": "mermaid"})
                    new_tag.append(content)
                    # replace the parent:
                    tag.parent.replaceWith(new_tag)
            # Count the diagrams <div class = 'mermaid'> ... </div>
            mermaids = len(soup.select("div.mermaid"))
        # if yes, add the javascript snippets:
        if mermaids:
            debug(
                "Page '%s': found %s diagrams, adding scripts" % (page_name, mermaids)
            )
            self.increment(count=mermaids)
            if not self.extra_mermaid_lib:
                # if no extra library mentioned specify it
                new_tag = soup.new_tag("script", src=self.mermaid_lib)
                soup.body.append(new_tag)
                # info(new_tag)
            new_tag = soup.new_tag("script")
            # initialization command
            new_tag.string = self.js_content
            soup.body.append(new_tag)
        return str(soup)

    def on_post_build(self, config):
        """
        Log total count after built
        """

        info("Found %s diagrams" % self.total_count)

    # ------------------------
    # Private
    # ------------------------
    def __initialize(self, config):
        self.__setup_custom_loader(config=config)
        self.__setup_extra_mermaid_lib(config=config)
        self.__setup_mermaid_lib()
        self.__setup_js_content()
        self._mermaids_count = 0

    def __setup_custom_loader(self, config):
        self._activate_custom_loader = False
        superfences_installed = SUPERFENCES_EXTENSION in config["markdown_extensions"]
        if not superfences_installed:
            return
        # get the config extension configs
        mdx_configs = config["mdx_configs"]
        # get the superfences config, if exists:
        superfence_config = mdx_configs.get(SUPERFENCES_EXTENSION)
        if not superfence_config:
            return

        debug("Found superfences config: %s" % superfence_config)
        custom_fences = superfence_config.get("custom_fences", [])
        for fence in custom_fences:
            format_fn = fence.get("format")
            if format_fn.__name__ != CUSTOM_FENCE_FN:
                continue
            self._activate_custom_loader = True
            debug(
                "Found '%s' function: "
                "activate custom loader for superfences" % CUSTOM_FENCE_FN
            )
            break

    def __setup_extra_mermaid_lib(self, config):
        extra_javascript = config.get("extra_javascript", [])
        for lib in extra_javascript:
            # get the actual library name
            if libname(lib) == "mermaid":
                self._extra_mermaid_lib = lib
                return
        self._extra_mermaid_lib = ""

    def __setup_mermaid_lib(self):
        mermaid_version = self.config["version"]
        lib = self.extra_mermaid_lib or MERMAID_LIB % mermaid_version
        if not url_exists(lib):
            raise FileNotFoundError("Cannot find Mermaid library: %s" % lib)
        self._mermaid_lib = lib

    def __setup_js_content(self):
        if self.activate_custom_loader:
            # if the superfences extension is present, use the specific loader
            self.mermaid_args["startOnLoad"] = False
            js_args = pyjs.dumps(self.mermaid_args)
            # new_tag.string = "window.mermaidConfig = {\n    default: %s\n}" % js_args
            self._js_content = "window.mermaidConfig = {default: %s}" % js_args
        else:
            js_args = pyjs.dumps(self.mermaid_args)
            self._js_content = "mermaid.initialize(%s);" % js_args

    def increment(self, count: int):
        """
        Record total count for logging
        """
        self._mermaids_count += count
