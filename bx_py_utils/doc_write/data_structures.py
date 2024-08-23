import dataclasses
from pathlib import Path


@dataclasses.dataclass
class GeneratedInfo:
    update_count: int
    remove_count: int
    paths: list[Path]


@dataclasses.dataclass
class DocuwriteConfig:
    """DocWrite: bx_py_utils/doc_write/README.md ## pyproject.toml settings [tool.doc_write] example
    ```
    [tool.bx_py_utils.doc_write]
    docstring_prefix = 'DocWrite:'
    macro_prefix = 'DocWriteMacro:'
    output_base_path = './docs/'
    search_paths = ['./foo/', './bar/']
    delete_obsolete_files = false  # Delete obsolete files in output_base_path
    ```
    Warning: Turn `delete_obsolete_files` only on if output_base_path is exclusively used by Doc-Write.

    Defaults are:
    DocWriteMacro: bx_py_utils_tests.doc_write_macros.config_defaults
    """

    base_path: Path
    search_paths: list[Path]
    output_base_path: Path
    docstring_prefix: str = 'DocWrite:'
    macro_prefix: str = 'DocWriteMacro:'
    delete_obsolete_files: bool = False  # Delete obsolete files in output_base_path

    def __post_init__(self):
        self.base_path = self.base_path.resolve(strict=True)

        self.search_paths = [Path(self.base_path / path).resolve(strict=False) for path in self.search_paths]
        self.search_paths = [path for path in self.search_paths if path.is_dir()]

        self.output_base_path = Path(self.base_path / self.output_base_path).resolve(strict=False)


@dataclasses.dataclass
class MacroContext:
    """
    DocWrite: bx_py_utils/doc_write/README.md ## Macros - context
    All macro functions will get a `MacroContext` dataclass instance as keyword argument with the following attributes:

    DocWriteMacro: bx_py_utils_tests.doc_write_macros.add_context_attributes
    """

    config: DocuwriteConfig
    path: str
    headline: str
    doc_string: str
