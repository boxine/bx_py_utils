from __future__ import annotations

import dataclasses
import logging
from pathlib import Path

from bx_py_utils.pyproject_toml import get_pyproject_config


logger = logging.getLogger(__name__)


DEFAULT_CFG = {
    'search_paths': ['.'],  # List of search paths for source files
    'output_base_path': './docs/',  # Base path for *.md output files
}


@dataclasses.dataclass
class DocuwriteConfig:
    """DocWrite: bx_py_utils/doc_write/README.md ## pyproject.toml settings [tool.doc_write] example
    ```
    [tool.bx_py_utils.doc_write]
    docstring_prefix = 'DocWrite:'
    output_base_path = './docs/'
    search_paths = ['./foo/', './bar/']
    delete_obsolete_files = false  # Delete obsolete files in output_base_path
    ```
    Warning: Turn `delete_obsolete_files` only on if output_base_path is excursively used by Doc-Write.
    """

    base_path: Path
    search_paths: list[Path]
    output_base_path: Path
    docstring_prefix: str = 'DocWrite:'
    delete_obsolete_files: bool = False  # Delete obsolete files in output_base_path

    def __post_init__(self):
        self.base_path = self.base_path.resolve(strict=True)

        self.search_paths = [Path(self.base_path / path).resolve(strict=False) for path in self.search_paths]
        self.search_paths = [path for path in self.search_paths if path.is_dir()]

        self.output_base_path = Path(self.base_path / self.output_base_path).resolve(strict=False)


def get_docu_write_cfg(base_path: Path | None = None) -> DocuwriteConfig:
    """DocWrite: bx_py_utils/doc_write/README.md ## pyproject.toml settings
    Add a section `[tool.doc_write]` to your `pyproject.toml` to configure Doc-Write.
    """
    if base_path is None:
        base_path = Path.cwd()

    docu_write_cfg = get_pyproject_config(base_path=base_path, section=('tool', 'bx_py_utils', 'doc_write'))
    if not docu_write_cfg:
        logger.info('No [tool.doc_write] found in pyproject.toml, use default.')
        docu_write_cfg = DEFAULT_CFG

    return DocuwriteConfig(base_path=base_path, **docu_write_cfg)
