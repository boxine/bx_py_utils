from __future__ import annotations

import logging
from pathlib import Path

from bx_py_utils.doc_write.data_structures import DocuwriteConfig
from bx_py_utils.pyproject_toml import get_pyproject_config


logger = logging.getLogger(__name__)


DEFAULT_CFG = {
    'search_paths': ['.'],  # List of search paths for source files
    'output_base_path': './docs/',  # Base path for *.md output files
}


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
