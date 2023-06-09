import inspect
import tempfile
from pathlib import Path
from unittest import TestCase

from bx_py_utils.doc_write.api import generate
from bx_py_utils.doc_write.cfg import DocuwriteConfig, get_docu_write_cfg


class DocuWriteApiTestCase(TestCase):
    def test_happy_path(self):
        with tempfile.TemporaryDirectory(prefix='docu-write-test') as tmp:
            temp_path = Path(tmp)

            pyproject_toml_path = temp_path / 'pyproject.toml'
            pyproject_toml_path.write_text(
                inspect.cleandoc(
                    """
                    [tool.bx_py_utils.doc_write]
                    docstring_prefix = 'TestDocs:'
                    output_base_path = './docs/'
                    search_paths = ['./not-exists/', './foo/', './bar/']
                    """
                )
            )
            foo_file_path = temp_path / 'foo' / 'test.py'
            foo_file_path.parent.mkdir()
            foo_file_path.write_text(
                inspect.cleandoc(
                    """
                    '''TestDocs: test/README.md # Headline 1
                    The Doc String 1
                    '''
                    """
                )
            )
            bar_file_path = temp_path / 'bar' / 'test1.py'
            bar_file_path.parent.mkdir()
            bar_file_path.write_text(
                inspect.cleandoc(
                    """
                    '''TestDocs: test/README.md # Headline 1
                    Merged Text to Headline 1
                    '''
                    """
                )
            )
            bar_file_path = temp_path / 'bar' / 'test2.py'
            bar_file_path.write_text(
                inspect.cleandoc(
                    """
                    '''TestDocs: test/README.md ## Headline 2
                    A second text block.
                    '''
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
                    output_base_path=temp_path / 'docs',
                    docstring_prefix='TestDocs:',
                ),
            )

            created_readme_path = temp_path / 'docs/test/README.md'
            self.assertIs(created_readme_path.exists(), False)
            doc_paths = generate(base_path=temp_path)
            self.assertEqual(doc_paths, [created_readme_path])
            generated_content = created_readme_path.read_text(encoding='UTF-8')
            self.assertEqual(
                generated_content,
                inspect.cleandoc(
                    """
                    # Headline 1

                    The Doc String 1

                    Merged Text to Headline 1

                    ## Headline 2

                    A second text block.
                    """
                ),
            )
