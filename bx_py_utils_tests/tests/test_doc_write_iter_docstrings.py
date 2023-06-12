"""
    1. Test for bx_py_utils.docuwrite.docstrings.iter_docstrings()
    This is in a separate file, because all DocStrings are
    a part of this test!
"""
from pathlib import Path
from unittest import TestCase

from bx_py_utils.doc_write.docstrings import iter_docstrings


class DocuWriteTestCase(TestCase):
    def test_iter_docstrings(self):
        """
        2. A class method single file, doc string
        """
        doc_strings = list(iter_docstrings(file_path=Path(__file__)))
        # Now we should have all DocStrings, isn't it?
        # Note: comments, like this, are no DocStrings -> will be ignored

        """
        3. This DocString should be collected, too.
        """

        def noop():
            """
            4. The Noop func DocString.
            """
            pass

        self.assertEqual(
            doc_strings,
            [
                (
                    '1. Test for bx_py_utils.docuwrite.docstrings.iter_docstrings()\n'
                    'This is in a separate file, because all DocStrings are\n'
                    'a part of this test!'
                ),
                '2. A class method single file, doc string',
                '3. This DocString should be collected, too.',
                '4. The Noop func DocString.',
            ],
        )
