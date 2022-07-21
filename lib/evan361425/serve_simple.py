"""
Main plugin module for simply serve dev mode
"""

from os import environ, getpid, path
from pathlib import Path
from mkdocs.plugins import BasePlugin

from json import load
from shutil import copyfile, copytree, rmtree

# ------------------------
# Constants and utilities
# ------------------------
SETTING_NAME = "serve.json"

# ------------------------
# Plugin
# ------------------------
class MarkdownServeSimplePlugin(BasePlugin):
    def on_config(self, config):
        # only support on development
        if (
            not config["site_url"].startswith("http://127.0.0.1")
            or "MKDOCS_SERVE_ALL" in environ
        ):
            return

        pid = str(getpid())
        src = config["docs_dir"] + "/"

        setting = self.__parse_setting(config)
        dest = replace_last_file(config["docs_dir"], setting["dest"])
        config["docs_dir"] = dest

        # Check exist
        if path.exists(dest + "/pid"):
            with open(dest + "/pid", "r") as pidF:
                if pidF.read() == pid:
                    return config

        # Recreate
        rmtree(dest)
        Path(dest).mkdir(parents=True, exist_ok=True)
        with open(dest + "/pid", "w") as pidF:
            pidF.write(pid)

        # copy
        for target in setting["targets"]:
            f = copytree if target.endswith("/") else copyfile
            if not target.endswith("/") and target.find("/") != -1:
                Path(dest + "/" + replace_last_file(target, "")).mkdir(
                    parents=True, exist_ok=True
                )
            f(src + target, dest + "/" + target)

        return config

    def __parse_setting(self, config):
        file_name = replace_last_file(config["config_file_path"], SETTING_NAME)
        with open(file_name) as json_file:
            return load(json_file)


def replace_last_file(path: str, name: str):
    index = path.rfind("/")
    return path[0 : index + 1] + name
