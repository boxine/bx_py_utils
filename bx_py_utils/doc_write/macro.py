import logging
import re
from collections.abc import Iterable

from bx_py_utils.doc_write.data_structures import MacroContext
from bx_py_utils.import_utils import import_string


logger = logging.getLogger(__name__)


class CallMacro:
    def __init__(self, macro_context: MacroContext):
        self.macro_context = macro_context

    def __call__(self, match):
        dotted_path = match.group(1)
        logger.info('Call macro function %r', dotted_path)

        macro_func = import_string(dotted_path)

        try:
            result = macro_func(macro_context=self.macro_context)
        except Exception as err:
            raise Exception(f'Call macro {dotted_path!r} error: {err}') from err

        """
        DocWrite: bx_py_utils/doc_write/README.md ## Macros
        Macro functions must return a string or an iterable of strings.
        """

        if isinstance(result, str):
            return result
        if isinstance(result, Iterable):
            try:
                return '\n'.join(part for part in result)
            except TypeError as err:
                raise TypeError(f'Error consuming macro {dotted_path!r}: {err}') from err
        else:
            raise TypeError(f'Macro {dotted_path!r} must return str or Iterable[str], not {type(result).__name__}')


def process_macros(*, macro_context: MacroContext):
    """
    DocWrite: bx_py_utils/doc_write/README.md ## Macros
    It's possible to define callables in the DocString block by using the `DocWriteMacro:` prefix
    and the callable name as dotting path. e.g.:

        DocWriteMacro: foo.bar.baz

    Example:

    ```
    DocWriteMacro: bx_py_utils_tests.doc_write_macros.macro_example_sources
    ```
    """
    config = macro_context.config
    macro_prefix = config.macro_prefix
    call_macro = CallMacro(macro_context)
    doc_string = re.sub(
        rf'^{macro_prefix}\s*([a-zA-Z0-9_.]+)\s*$',
        call_macro,
        macro_context.doc_string,
        flags=re.MULTILINE | re.DOTALL,
    )
    return doc_string
