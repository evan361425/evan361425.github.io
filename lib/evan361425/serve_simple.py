"""
Main plugin module for simply serve dev mode
"""

from json import load
from shutil import rmtree
from os import environ, getpid, listdir, path, symlink
from pathlib import Path
from mkdocs.plugins import BasePlugin


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
            with open(dest + "/pid", "r", encoding="utf-8") as pid_f:
                if pid_f.read() == pid:
                    return config

        # Recreate
        rmtree(dest)
        Path(dest).mkdir(parents=True, exist_ok=True)
        with open(dest + "/pid", "w", encoding="utf-8") as pid_f:
            pid_f.write(pid)

        # copy
        for target in setting["targets"]:
            if target.find("/") != -1:
                file_path = Path(path.join(dest, replace_last_file(target, "")))
                file_path.mkdir(parents=True, exist_ok=True)
            files = (
                [path.join(target, f) for f in listdir(src + target)]
                if target.endswith("/")
                else [target]
            )
            for file in files:
                symlink(path.join(src, file), path.join(dest, file))

        return config

    def __parse_setting(self, config):
        file_name = replace_last_file(config["config_file_path"], SETTING_NAME)
        with open(file_name, encoding="utf-8") as json_file:
            return load(json_file)


def replace_last_file(file_path: str, name: str):
    index = file_path.rfind("/")
    return file_path[0 : index + 1] + name
