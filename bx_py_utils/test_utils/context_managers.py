class MassContextManager:
    """
    A context manager that enter/exit a list of mocks.
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
        for mock in self.mocks:
            mock.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.mocks
        for mock in self.mocks:
            mock.__exit__(exc_type, exc_val, exc_tb)
