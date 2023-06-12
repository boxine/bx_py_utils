from __future__ import annotations

from pathlib import Path

from bx_py_utils.doc_write.api import generate


def main(base_path: Path | None = None):
    """DocWrite: bx_py_utils/doc_write/README.md ## Usage
    To write your doc files, just call, e.g.:

    ```
    ~/your-project-src$ python3 -m bx_py_utils.doc_write
    ```

    You can also compile the documentation via code, e.g.:
    ```
    from bx_py_utils.doc_write.api import generate

    generate()
    ```
    """

    generate(base_path=base_path)


if __name__ == '__main__':
    main()
