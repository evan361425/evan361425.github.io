import logging

# -------------------
# Logging
# -------------------
log = logging.getLogger("mkdocs.plugins." + __name__)

LABEL = "Custom -"  # plugin's signature label


def info(*args) -> str:
    "Write information on the console, preceded by the signature label"
    args = [LABEL] + [str(arg) for arg in args]
    msg = " ".join(args)
    log.info(msg)


def debug(*args) -> str:
    "Write debug on the console, preceded by the signature label"
    args = [LABEL] + [str(arg) for arg in args]
    msg = " ".join(args)
    log.debug(msg)
