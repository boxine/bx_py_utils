from contextlib import ContextDecorator


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
        for mock in self.mocks:
            mock.__exit__(exc_type, exc_val, exc_tb)
