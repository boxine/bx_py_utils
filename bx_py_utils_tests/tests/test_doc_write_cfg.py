import inspect
import tempfile
from pathlib import Path
from unittest import TestCase

from bx_py_utils.doc_write.cfg import DocuwriteConfig, get_docu_write_cfg


class DocuWriteCfgTestCase(TestCase):
    def test_happy_path(self):
        with tempfile.TemporaryDirectory(prefix='docu-write-test') as tmp:
            temp_path = Path(tmp)
            default_cfg = get_docu_write_cfg(base_path=temp_path)
            self.assertEqual(
                default_cfg,
                DocuwriteConfig(
                    base_path=temp_path,
                    search_paths=[temp_path],
                    output_base_path=temp_path / 'docs',
                    docstring_prefix='DocWrite:',
                ),
            )

            pyproject_toml_path = temp_path / 'pyproject.toml'
            pyproject_toml_path.write_text(
                inspect.cleandoc(
                    """
                    [tool.bx_py_utils.doc_write]
                    docstring_prefix = 'TestDocs:'
                    output_base_path = './documentation/'
                    search_paths = ['./not-exists/', './foo/', './bar/']
                    """
                )
            )
            config = get_docu_write_cfg(base_path=temp_path)
            self.assertEqual(
                config,
                DocuwriteConfig(
                    base_path=temp_path,
                    search_paths=[
                        temp_path / 'foo',
                        temp_path / 'bar',
                    ],
                    output_base_path=temp_path / 'documentation',
                    docstring_prefix='TestDocs:',
                ),
            )
