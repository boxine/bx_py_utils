"""
    DocWrite: bx_py_utils/doc_write/README.md ## Macros

    The recommendation is not to include the macro functions in the package.
    A good place could be next to the tests.
    e.g: The bx_py_utils own used doc write macros are stored in:

    * `bx_py_utils_tests/doc_write_macros.py`
"""

import dataclasses
import inspect

from bx_py_utils.doc_write.data_structures import MacroContext


def add_context_attributes(macro_context: MacroContext):
    """
    Add MacroContext attributes to the documentation.
    """
    for field in dataclasses.fields(macro_context):
        yield f' * {field.name}: {field.type.__name__}'


def macro_example_sources(macro_context: MacroContext):
    """
    Adds `add_context_attributes` source code as a example to the documentation.
    """
    return inspect.getsource(add_context_attributes)


def config_defaults(macro_context: MacroContext):
    """
    Add the default values of the `DocuwriteConfig` dataclass to the documentation.
    """
    for field in dataclasses.fields(macro_context.config):
        if field.default is dataclasses.MISSING:
            continue

        value = getattr(macro_context.config, field.name)
        yield f' * `{field.name}`: `{value!r}`'
