# https://gist.github.com/Chiron1991/8199fc1a41c2107982053aba809838c6
#
# tests functions from the gist were moved to utilities.tests.test_processify
# so they can be picked up by our test runner

import sys
import traceback
from functools import wraps
from multiprocessing import Process, Queue


class _ProcessifyWrapper:
    # Top-level class so instances are picklable under forkserver/spawn start methods
    # (Python 3.14+ changed the default from fork to forkserver on Linux).
    # Stores only the function's module and qualname (strings) to avoid pickle
    # identity problems caused by @wraps replacing the module-level name.
    def __init__(self, module, qualname):
        self.module = module
        self.qualname = qualname

    def __call__(self, q, *args, **kwargs):
        import importlib

        mod = importlib.import_module(self.module)
        obj = mod
        for part in self.qualname.split('.'):
            obj = getattr(obj, part)
        # @wraps sets __wrapped__ to the original function; unwrap to avoid
        # calling the processify wrapper recursively in the subprocess.
        func = getattr(obj, '__wrapped__', obj)
        try:
            ret = func(*args, **kwargs)
        except Exception:
            ex_type, ex_value, tb = sys.exc_info()
            error = ex_type, ex_value, ''.join(traceback.format_tb(tb))
            ret = None
        else:
            error = None
        q.put((ret, error))


def processify(func):
    """
    Decorator to run a function as a process.
    Be sure that every argument and the return value
    is *pickable*.
    The created process is joined, so the code does not
    run in parallel.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        q = Queue()
        p = Process(target=_ProcessifyWrapper(func.__module__, func.__qualname__), args=(q,) + args, kwargs=kwargs)
        p.start()
        ret, error = q.get()
        p.join()

        if error:
            ex_type, ex_value, tb_str = error
            message = f'{ex_value!s} (in subprocess)\n{tb_str}'
            raise ex_type(message)

        return ret

    return wrapper
