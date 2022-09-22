import fnmatch
import importlib
import inspect
import re
from pathlib import Path

from pdoc import extract
from pdoc.doc import Module

from bx_py_utils.test_utils.assertion import assert_text_equal


class ModulePath:
    def __init__(self):
        self.cache = {}

    def get_base_path(self, module_name):
        base_module = module_name.partition('.')[0]
        if base_module not in self.cache:
            module = importlib.import_module(base_module)
            module_path = Path(module.__file__).parent
            self.cache[base_module] = module_path
            return module_path
        return self.cache[base_module]


def get_code_location(obj):
    """
    Return start and end line number for an object via inspect.
    """
    lines, start = inspect.getsourcelines(obj)
    return start, start + len(lines) - 1


def generate_modules_doc(modules, exclude_func: callable = None, start_level=1, link_template=None):
    """
    Generate a list of function/class information via pdoc.

    :param modules: module specifications for pdoc.extract.walk_specs()
    :param exclude_func: A callable to filter the files
    :param start_level: Markdown "#" min. count
    :param link_template: String that can generate a URL with: {path}, {start}, {end} placeholder
    """
    if link_template and 'lnum' in link_template:
        raise AssertionError('Please change "lnum" in "link_template" to {start}, {end}')

    def first_doc_line(doc_string):
        try:
            return doc_string.splitlines()[0]
        except IndexError:
            return None

    def get_doc_list(pdoc_list, root_path):
        for pdoc_item in sorted(pdoc_list):
            item_name = pdoc_item.name
            if item_name.startswith('_'):
                continue

            item_doc_line = first_doc_line(pdoc_item.docstring)
            if not item_doc_line:
                continue

            item_name = f'`{item_name}()`'

            if link_template:
                item_path = Path(pdoc_item.source_file)
                path = item_path.relative_to(root_path)

                start, end = get_code_location(obj=pdoc_item.obj)
                link = link_template.format(
                    path=path,
                    start=start,
                    end=end,
                )
                item_name = f'[{item_name}]({link})'

            yield f'* {item_name} - {item_doc_line}\n'

    module_path = ModulePath()

    module_names = extract.walk_specs(modules)
    parts = []
    for module_name in sorted(module_names):
        module_obj = extract.load_module(module_name)
        if exclude_func is not None and not exclude_func(module_obj.__file__):
            # This file should be excluded
            continue

        base_path = module_path.get_base_path(module_name=module_name)
        module_root_path = base_path.parent

        pdoc_module = Module(module_obj)

        # Collect information

        module_doc_line = first_doc_line(pdoc_module.docstring)

        class_docs = list(get_doc_list(pdoc_list=pdoc_module.classes, root_path=module_root_path))
        func_docs = list(get_doc_list(pdoc_list=pdoc_module.functions, root_path=module_root_path))

        # Generate output only if information exists:

        if module_doc_line or class_docs or func_docs:
            level = module_name.count('.') + start_level
            parts.append(f'\n{"#" * level} {module_name}\n\n')

        if module_doc_line:
            parts.append(f'{module_doc_line}\n\n')

        parts.extend(class_docs)
        parts.extend(func_docs)
    return ''.join(parts)


def assert_readme(
    readme_path: Path,
    modules: list,
    exclude_func: callable = None,
    start_marker_line: str = '[comment]: <> (✂✂✂ auto generated start ✂✂✂)',
    end_marker_line: str = '[comment]: <> (✂✂✂ auto generated end ✂✂✂)',
    start_level: int = 1,
    link_template: str = None,
):
    """
    Check and update README file with generate_modules_doc()
    The automatic generated documentation list will be "replace" between the given markers.
    """
    assert readme_path.is_file()
    old_readme = readme_path.read_text()

    assert start_marker_line in old_readme
    assert end_marker_line in old_readme

    doc_block = generate_modules_doc(
        modules=modules,
        exclude_func=exclude_func,
        start_level=start_level,
        link_template=link_template,
    )

    doc_block = f'{start_marker_line}\n{doc_block}\n{end_marker_line}'

    start = re.escape(start_marker_line)
    end = re.escape(end_marker_line)

    new_readme, sub_count = re.subn(
        f'{start}(.*?){end}',
        doc_block,
        old_readme,
        flags=re.DOTALL
    )
    assert sub_count == 1
    if old_readme != new_readme:
        readme_path.write_text(new_readme)

        # display error message with diff:
        assert_text_equal(old_readme, new_readme)


class FnmatchExclude:
    """
    Helper for auto doc `exclude_func` that exclude files via fnmatch pattern.
    """

    def __init__(self, *patterns):
        self.patterns = patterns

    def __call__(self, file_path: str) -> bool:
        assert isinstance(file_path, str)
        for pattern in self.patterns:
            assert isinstance(pattern, str)
            if fnmatch.fnmatch(file_path, pattern):
                return False  # ignore this file for auto docs
        return True  # include this file
