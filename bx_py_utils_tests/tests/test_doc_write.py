from pathlib import Path
from unittest import TestCase

import bx_py_utils
from bx_py_utils.doc_write.api import generate
from bx_py_utils.path import assert_is_file


class DocuWriteApiTestCase(TestCase):
    def test_up2date_docs(self):
        """
        Just generate "Doc-Write" files, to have always up2date documentation files.
        """
        base_path = Path(bx_py_utils.__file__).parent.parent
        assert_is_file(base_path / 'pyproject.toml')

        doc_paths = generate(base_path=base_path)
        self.assertGreaterEqual(len(doc_paths), 1)
