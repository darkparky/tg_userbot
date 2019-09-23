""" Init file which loads all of the utilities """
from userbot import LOGS

def __list_all_utils():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_utils = [
        basename(f)[:-3] for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_utils


ALL_UTILS = sorted(__list_all_utils())
LOGS.info("Utilities to load: %s", str(ALL_UTILS))
__all__ = ALL_UTILS + ["ALL_UTILS"]
