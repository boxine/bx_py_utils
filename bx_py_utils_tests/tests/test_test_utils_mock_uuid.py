import uuid
from unittest import TestCase

from bx_py_utils.test_utils.mock_uuid import MockUUIDGenerator


class UUIDMockTest(TestCase):
    def test_basics(self):
        with MockUUIDGenerator.install():
            self.assertEqual(uuid.uuid4(), uuid.UUID('89e6b14d-622a-409f-88de-000000000001'))
            self.assertEqual(uuid.uuid4(), uuid.UUID('89e6b14d-622a-409f-88de-000000000002'))
            self.assertEqual(uuid.uuid4(), uuid.UUID('89e6b14d-622a-409f-88de-000000000003'))
