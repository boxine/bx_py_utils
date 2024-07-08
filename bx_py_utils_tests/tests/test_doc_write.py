from pathlib import Path
from unittest import TestCase

import bx_py_utils
from bx_py_utils.doc_write.api import GeneratedInfo, generate
from bx_py_utils.path import assert_is_file


class DocuWriteApiTestCase(TestCase):
    def test_up2date_docs(self):
        """DocWrite: bx_py_utils/doc_write/README.md ## Usage
        Tip: Just include "generate Doc-Write" files" into your unittests.
        So you have always up2date documentation files.

        Example for a unittest can be found here:

        https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils_tests/tests/test_doc_write.py
        """
        base_path = Path(bx_py_utils.__file__).parent.parent
        assert_is_file(base_path / 'pyproject.toml')

        info: GeneratedInfo = generate(base_path=base_path)
        self.assertGreaterEqual(len(info.paths), 1)
        self.assertEqual(info.update_count, 0, 'No files should be updated, commit the changes')
        self.assertEqual(info.remove_count, 0, 'No files should be removed, commit the changes')
