import contextlib
import io

from bx_py_utils.test_utils.context_managers import MassContextManager


class RedirectOut(MassContextManager):
    """
    Redirect stdout + stderr into a buffer (with optional strip the output)
    """

    def __init__(self, strip=False):
        self.strip = strip

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
