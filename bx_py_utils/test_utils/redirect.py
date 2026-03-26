import contextlib
import io
import sys

from bx_py_utils.test_utils.context_managers import MassContextManager


class RedirectOut(MassContextManager):
    """
    Redirect stdout + stderr into a buffer (with optional strip the output)
    In case of an exception, the captured output will be printed to the original stderr as default.
    """

    def __init__(self, strip=False, exception_fallback_print=True):
        self.strip = strip
        self.exception_fallback_print = exception_fallback_print

        self.origin_stderr = sys.stderr

        self._stdout_buffer = io.StringIO()
        self._stderr_buffer = io.StringIO()
        self.mocks = (
            contextlib.redirect_stdout(self._stdout_buffer),
            contextlib.redirect_stderr(self._stderr_buffer),
        )

    def _output(self, buffer):
        output = buffer.getvalue()
        if self.strip:
            output = output.strip()
        return output

    @property
    def stdout(self) -> str:
        return self._output(buffer=self._stdout_buffer)

    @property
    def stderr(self) -> str:
        return self._output(buffer=self._stderr_buffer)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.exception_fallback_print:
            print(
                f'Exception raised while buffer {exc_type.__name__}: {exc_val}\n'
                '∨∨∨∨∨∨∨∨∨∨∨∨ [captured stdout+err] ∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨∨\n'
                f'{self.stdout.strip()}\n'
                f'{self.stderr.strip()}\n'
                '∧∧∧∧∧∧∧∧∧∧∧∧ [captured stdout+err] ∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧\n'
                '\n',
                file=self.origin_stderr,
            )
        return super().__exit__(exc_type, exc_val, exc_tb)
