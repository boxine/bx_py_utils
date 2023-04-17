import inspect
import tempfile
from pathlib import Path
from unittest import TestCase

from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.test_utils.assertion import assert_text_equal


class AutoDocTestCase(TestCase):
    def test_assert_readme_block(self):
        text_block = inspect.cleandoc(
            '''
            This is just a few
            lines of test text.
            '''
        )
        start_marker_line = '[comment]: <> (✂✂✂ auto generated start ✂✂✂)'
        end_marker_line = '[comment]: <> (✂✂✂ auto generated end ✂✂✂)'

        with self.assertRaises(NotADirectoryError):
            assert_readme_block(
                readme_path=Path('does/not/exists'),
                text_block=text_block,
                start_marker_line=start_marker_line,
                end_marker_line=end_marker_line,
            )

        with tempfile.NamedTemporaryFile(prefix='test_assert_readme_block', suffix='.md') as f:
            readme_path = Path(f.name)
            with self.assertRaises(AssertionError) as cm:
                assert_readme_block(
                    readme_path=readme_path,
                    text_block=text_block,
                    start_marker_line=start_marker_line,
                    end_marker_line=end_marker_line,
                )
            error_message = str(cm.exception)
            self.assertIn(
                "Start marker '[comment]: <> (✂✂✂ auto generated start ✂✂✂)' not found in:",
                error_message,
            )

            readme_path.write_text(
                inspect.cleandoc(
                    '''
                    # Prefix Text

                    [comment]: <> (✂✂✂ auto generated start ✂✂✂)
                    '''
                )
            )

            with self.assertRaises(AssertionError) as cm:
                assert_readme_block(
                    readme_path=readme_path,
                    text_block=text_block,
                    start_marker_line=start_marker_line,
                    end_marker_line=end_marker_line,
                )
            error_message = str(cm.exception)
            self.assertIn(
                "End marker '[comment]: <> (✂✂✂ auto generated end ✂✂✂)' not found in:",
                error_message,
            )

            readme_path.write_text(
                inspect.cleandoc(
                    '''
                    # Prefix Text

                    [comment]: <> (✂✂✂ auto generated start ✂✂✂)
                    [comment]: <> (✂✂✂ auto generated end ✂✂✂)

                    Suffix text
                    '''
                )
            )

            with self.assertRaises(AssertionError) as cm:
                assert_readme_block(
                    readme_path=readme_path,
                    text_block=text_block,
                    start_marker_line=start_marker_line,
                    end_marker_line=end_marker_line,
                )
            error_message = str(cm.exception)
            self.assertIn(
                'Text not equal:',
                error_message,
            )

            result = readme_path.read_text()
            assert_text_equal(
                result,
                inspect.cleandoc(
                    '''
                    # Prefix Text

                    [comment]: <> (✂✂✂ auto generated start ✂✂✂)
                    This is just a few
                    lines of test text.
                    [comment]: <> (✂✂✂ auto generated end ✂✂✂)

                    Suffix text
                    '''
                ),
            )
