import inspect
import tempfile
from pathlib import Path
from unittest import TestCase

from bx_py_utils.doc_write.api import generate
from bx_py_utils.doc_write.cfg import DocuwriteConfig, get_docu_write_cfg
from bx_py_utils.path import assert_is_file


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
                    The Doc String 2 (from foo)
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
                    Merged Text to Headline 1 (from bar)
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
                        # intentionally not in alphabetical order
                        temp_path / 'foo',
                        temp_path / 'bar',
                    ],
                    output_base_path=temp_path / 'docs',
                    docstring_prefix='TestDocs:',
                ),
            )

            # Create an "obsolete" file:
            obsolete_md_path = temp_path / 'docs/test/obsolete.md'
            obsolete_md_path.parent.mkdir(parents=True, exist_ok=False)
            obsolete_md_path.touch()

            created_readme_path = temp_path / 'docs/test/README.md'
            self.assertIs(created_readme_path.exists(), False)
            doc_paths = generate(base_path=temp_path)
            self.assertEqual(doc_paths, [created_readme_path])
            generated_content = created_readme_path.read_text()
            self.assertEqual(
                generated_content,
                inspect.cleandoc(
                    """
                    # Headline 1

                    Merged Text to Headline 1 (from bar)

                    The Doc String 2 (from foo)

                    ## Headline 2

                    A second text block.
                    """
                ),
            )

            # The default is not to delete obsolete files -> does it still exists?
            assert_is_file(obsolete_md_path)

            # Activate deleting of obsolete files:
            with pyproject_toml_path.open('a') as f:
                f.write('\ndelete_obsolete_files = true\n')

            # Run again and delete obsolete files:
            generate(base_path=temp_path)

            # Obsolete file removed?
            self.assertIs(obsolete_md_path.exists(), False)

            # readme is still the same?
            self.assertEqual(created_readme_path.read_text(), generated_content)
