from contextlib import ContextDecorator


class MassContextManagerExceptions(Exception):
    def __init__(self, exceptions):
        self.exceptions = exceptions


class MassContextManager(ContextDecorator):
    """
    A context manager / decorator that enter/exit a list of mocks.
    e.g.:
        class FooBarMocks(MassContextManager):
            mocks = (
                mock.patch('foo.bar', return_value='foo'),
                mock.patch('foo.baz', return_value='bar')
            )
    """

    mocks = ()  # Must be set in subclass

    def __enter__(self):
        assert self.mocks
        self.patchers = [mock.__enter__() for mock in self.mocks]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.mocks
        errors = []
        for mock in self.mocks:
            try:
                mock.__exit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                errors.append(e)
        if errors:
            raise MassContextManagerExceptions(errors)
