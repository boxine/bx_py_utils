# Based on Django's module_loading.py

import sys
from importlib import import_module


def cached_import(module_path, class_name):
    # Check whether module is loaded and fully initialized.
    if not (
        (module := sys.modules.get(module_path))
        and (spec := getattr(module, "__spec__", None))
        and getattr(spec, "_initializing", False) is False
    ):
        module = import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the last name in the path.
    Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(f'Module "{module_path}" does not define a "{class_name}" attribute/class') from err
