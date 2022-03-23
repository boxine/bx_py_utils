import uuid
from unittest import mock


class MockUUIDGenerator:
    """ Helper to mock `uuid.uuid4()` with reproducible results (e.g. for snapshot tests) """

    def __init__(self):
        self.num = 0

    def __call__(self):
        self.num += 1
        return uuid.UUID(f'89e6b14d-622a-409f-88de-{self.num:012d}')

    @classmethod
    def install(cls):
        instance = MockUUIDGenerator()
        return instance

    def __enter__(self):
        self._mock = mock.patch('uuid.uuid4', self)
        self._mock.__enter__()

    def __exit__(self, exc, value, tb):
        self._mock.__exit__(exc, value, tb)
