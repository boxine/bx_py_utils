import ast
import collections
import inspect
import logging
import re
from collections.abc import Iterator
from pathlib import Path

from bx_py_utils.doc_write.cfg import DocuwriteConfig
from bx_py_utils.doc_write.walk import iter_file_path


def get_docstring(node):  # Origin ast.get_docstring() will not collect all DocStrings!
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
        if text := node.value.s:
            if text := inspect.cleandoc(text).strip():
                return text


def iter_docstrings(file_path: Path) -> Iterator[str]:
    file_content = file_path.read_text(encoding='UTF-8')
    try:
        ast_tree = ast.parse(file_content)
    except SyntaxError as err:
        logging.error('SyntaxError in %s: %s', file_path, err)
        return
    for node in ast.walk(ast_tree):
        if doc_string := get_docstring(node):
            yield doc_string


def collect_docstrings(*, config: DocuwriteConfig) -> dict:
    """DocWrite: bx_py_utils/doc_write/README.md ### Howto
    All Doc-Strings that should be transferred by Doc-Write must start with a special line:
    ```
    {prefix} {file-path} # Headline text
    ```
    The meaning, broken down:
    * `{prefix}`: String defined as `docstring_prefix` in your `project.toml` file.
    * `{file-path}`: Relative file path to `output_base_path` and must point to a `*.md` file.
    * `# Headline text`: The DocString block will be merged under this headline.

    Notes:
    * `{file-path}` and headline must not be unique!
      The opposite is true: Documentation is assembled from different places!
    """
    regex = re.compile(config.docstring_prefix + r'\s*(.*?) (#{1,}.+?)\n+(.+)', re.DOTALL)

    storage = collections.defaultdict(dict)
    for file_path in sorted(iter_file_path(file_paths=config.search_paths, rglob_pattern='*.py')):
        for doc_string in iter_docstrings(file_path=file_path):
            if not doc_string.startswith(config.docstring_prefix):
                """DocWrite: bx_py_utils/doc_write/README.md ### Notes
                * All Doc-String without the `{prefix}` will be ignored.
                """
                continue

            match = regex.fullmatch(doc_string)
            if match:
                path, headline, doc_string = match.groups()
                if not path.endswith('.md'):
                    """DocWrite: bx_py_utils/doc_write/README.md ### Notes
                    * The `{file-path}` must has the file extension `.md`
                    Otherwise the DocString block will be ignored.
                    """
                    logging.error('Ignore non *.md docstring for: %s', path)
                    continue

                file_data = storage[path]
                if headline not in file_data:
                    file_data[headline] = [doc_string]
                else:
                    file_data[headline].append(doc_string)
            else:
                print('No match:', doc_string)

    return dict(storage)
