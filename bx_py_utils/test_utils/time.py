class MockTimeMonotonicGenerator:
    """
    Helper to mock `time.monotonic()`, `time.time()` etc. in tests.
    The default output is a float that starts at 1.0 and increases by 1.0

    e.g.:

    class FooBar(TestCase):
        @mock.patch.object(time, 'monotonic', MockTimeMonotonicGenerator())
        def test_something(self):
            print(time.monotonic())  # 1.0
            print(time.monotonic())  # 2.0
            ...

    You can also use it for monotonic_ns() that returns integers by set `cast_func`, e.g.:

        with mock.patch.object(time, 'monotonic_ns', MockTimeMonotonicGenerator(offset=100, cast_func=int)):
            print(time.monotonic_ns())  # 100
            print(time.monotonic_ns())  # 200
            ...
    """

    def __init__(self, offset=1, cast_func=float):
        self.offset = offset
        self.cast_func = cast_func
        self.num = 0

    def __call__(self):
        self.num += self.offset
        return self.cast_func(self.num)
