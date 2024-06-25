import os


_conversion_powers = {
    'KB': 1,
    'MB': 2,
    'GB': 3,
    'TB': 4,
}


def cgroup_memory_usage(unit='B', cgroup_mem_file='/sys/fs/cgroup/memory/memory.usage_in_bytes'):
    """
    Returns the memory usage of the cgroup the Python interpreter is running in.

    This is handy for getting the memory usage inside a Docker container since they are
    implemented using cgroups.
    With conventional tools (e.g. psutil) this is not possible, because they often rely on
    stats reported by /proc, but that one reports metrics from the host system.
    """
    with open(cgroup_mem_file, 'r') as infile:
        usage_bytes = infile.readline()
    usage_bytes = int(usage_bytes)

    if usage_bytes == 0 or unit == 'B':
        return usage_bytes

    return usage_bytes / 1024 ** _conversion_powers[unit]


class OverrideEnviron:
    """
    Context manager to change 'os.environ' temporarily.
    Set variable value to None to remove the variable.
    """

    def __init__(self, **overrides):
        self.overrides = overrides

    def __enter__(self):
        self._origin_env = os.environ.copy()
        for k, v in self.overrides.items():
            if v is None:
                # delete
                if k in os.environ:
                    del os.environ[k]
            else:
                assert isinstance(v, str), f'Value for {k} must be a string!'
                os.environ[k] = v

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise
        os.environ = self._origin_env  # noqa:B003
