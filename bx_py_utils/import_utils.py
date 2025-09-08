import sys
from importlib import import_module
from pathlib import Path

from bx_py_utils.path import assert_is_file


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
    Based on Django's module_loading.py
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(f'Module "{module_path}" does not define a "{class_name}" attribute/class') from err


def import_all_files(*, package: str, init_file: str) -> list:
    """
    Helper to import all Python files from a package. Helpful for registry via imports.

    For example: Implement Django Model Admin as a package.
    Add the following into, e.g.: .../mydjangoapp/admin/__init__.py

        import_all_files(package=__package__, init_file=__file__)
    """
    init_file_path = Path(init_file)
    assert_is_file(init_file_path)

    module_path = init_file_path.parent

    imported_names = []
    for item in module_path.glob('*.py'):
        file_name = item.stem
        if file_name.startswith('_'):
            continue

        name = f'{package}.{file_name}'
        import_module(name)
        imported_names.append(name)
    return imported_names
