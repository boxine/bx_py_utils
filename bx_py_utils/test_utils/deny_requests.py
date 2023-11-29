from unittest.mock import patch

from bx_py_utils.test_utils.context_managers import MassContextManager


class DenyCallError(SystemExit):
    """[no-doc]
    Error that will be raised on request usage. Based on SystemExit to be loud in tests ;)
    """


class DenyCall:
    """[no-doc]
    Will raise DenyCallError on request usage with information about the call.
    """

    def __init__(self, func_name):
        self.func_name = func_name

    def __call__(self, *args, **kwargs):
        raise DenyCallError(f'Deny {self.func_name} call with: {args=} {kwargs=}')


class DenyAnyRealRequestContextManager(MassContextManager):
    """
    Context manager that denies any request via docket/urllib3. Will raise DenyCallError.
    """

    mocks = (
        patch(  # all built-in modules used socket
            'socket.create_connection',
            DenyCall('socket create_connection()'),
        ),
        patch(  # requests used urllib3
            'urllib3.util.connection.create_connection',
            DenyCall('urllib3 create_connection()'),
        ),
    )


def deny_any_real_request():
    """
    Deny any request via docket/urllib3. Useful for tests, because they should mock all requests.
    In django you can add something like this into our test settings.py:

        if os.environ.get('REQUESTS_IN_TESTS') not in ('1', 'true'):
            deny_any_real_request()
    """
    cm = DenyAnyRealRequestContextManager()
    cm.__enter__()
