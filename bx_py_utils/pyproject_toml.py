from __future__ import annotations

from pathlib import Path

from bx_py_utils.dict_utils import dict_get


try:
    import tomllib  # New in Python 3.11
except ImportError:
    try:
        import tomli as tomllib
    except ImportError as err:
        raise ImportError(f'Please add "tomli" to your dev-dependencies! Origin error: {err}')


def get_pyproject_config(section: tuple[str, ...], base_path: Path | None = None) -> None | bool | str | dict | list:
    """
    Get a config section from "pyproject.toml". The path can be optional specify.
    Section is used to get the nested information, e.g.:

        [tool.foo]
        bar=123

    get_pyproject_config(section=('tool') -> {"foo": {"bar": 123}}
    get_pyproject_config(section=('tool', 'foo') -> {"bar": 123}
    get_pyproject_config(section=('tool', 'foo', 'bar') -> 123

    Returns None, if file not found or section/key path not exists.
    """
    if not base_path:
        base_path = Path.cwd()

    pyproject_toml_path = base_path / 'pyproject.toml'
    try:
        pyproject_text = pyproject_toml_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    else:
        pyproject_config = tomllib.loads(pyproject_text)
        return dict_get(pyproject_config, *section)
