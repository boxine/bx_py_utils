""" DocWrite: bx_py_utils/doc_write/README.md # Doc-Write: DocStrings -> Markdown files

    In short: Doc-Write transfers source code DocStrings into Markdown files.

    The philosophy is to add documentation as near to your code as possible.
    This is to ensure that the documentation is not out of date.
    If you change the code and the documentation is just above it,
    then hopefully you update it at the same time ;)

    A example looks like this:
    ```
    class FooBar:
        ''' DocWrite: README.md # This is the headline
        This Text will be added to: {output_base_path}/README.md
        '''
        pass
    ```

    This README is generated by Doc-Write.
    You can just search for the used prefix to find all code parts that contains DocStrings for this README.
    e.g.:
    * https://github.com/search?q=repo%3Aboxine%2Fbx_py_utils+%22DocWrite%3A%22&type=code
"""

from __future__ import annotations

import logging
from pathlib import Path

from bx_py_utils.doc_write.cfg import DocuwriteConfig, get_docu_write_cfg
from bx_py_utils.doc_write.docstrings import collect_docstrings


logger = logging.getLogger(__name__)


def generate(base_path: Path | None = None) -> list[Path]:
    config: DocuwriteConfig = get_docu_write_cfg(base_path=base_path)

    doc_paths = []
    docs_data = collect_docstrings(config=config)
    for rel_file_path, data in sorted(docs_data.items()):
        docs = []
        for headline, docstrings in sorted(data.items()):
            """DocWrite: bx_py_utils/doc_write/README.md ### Notes
            * Headlines will be sorted, so they appears ordered by the level.
            """
            docs.append(headline)
            docs.append('\n\n'.join(docstrings))
        merged_doc = '\n\n'.join(docs)

        """ DocWrite: bx_py_utils/doc_write/README.md ### Notes
        * The created created Markdown file is relative to `output_base_path` (defined in `pyproject.toml`)
        """
        out_path = config.output_base_path / rel_file_path
        logger.info('Write %s', out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(merged_doc, encoding='UTF-8')
        doc_paths.append(out_path)
    return doc_paths