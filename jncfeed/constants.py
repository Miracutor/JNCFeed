import sys
from pathlib import Path

# List of constant used by JNCFeed
IS_DEV = True


ICON_PATH_PROD = (Path(sys.executable).parent / Path("logo.ico")).absolute()
ICON_PATH_DEV = (
    Path(__file__).parent.parent / Path("media") / Path("logo.ico")
).absolute()


def get_icon_path():
    if IS_DEV:
        return ICON_PATH_DEV
    else:
        return ICON_PATH_PROD


CONFIG_DIR_PATH_PROD = Path.home() / Path(".jncfeed")
CONFIG_DIR_PATH_DEV = Path.home() / Path(".jncfeed_dev")


def get_config_dir_path():
    if IS_DEV:
        return CONFIG_DIR_PATH_DEV
    else:
        return CONFIG_DIR_PATH_PROD


ENTRY_LIMIT_PROD = 15
ENTRY_LIMIT_DEV = 3


def get_entry_limit():
    if IS_DEV:
        return ENTRY_LIMIT_DEV
    else:
        return ENTRY_LIMIT_PROD
