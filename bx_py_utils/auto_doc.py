import re
import sys
from pathlib import Path


try:
    from pdoc import extract
    from pdoc.doc import Module
except ImportError:
    if sys.version_info >= (3, 7):
        # pdoc is not compatible with Python 3.6
        raise


from bx_py_utils.test_utils.assertion import assert_text_equal


def generate_modules_doc(modules, start_level=1):
    """
    Generate a list of function/class information via pdoc.
    """
    assert sys.version_info >= (3, 7), 'pdoc is not compatible with Python 3.6'

    def first_doc_line(doc_string):
        try:
            return doc_string.splitlines()[0]
        except IndexError:
            return None

    def get_doc_list(pdoc_list):
        for pdoc_item in sorted(pdoc_list):
            item_name = pdoc_item.name
            if item_name.startswith('_'):
                continue
            item_doc_line = first_doc_line(pdoc_item.docstring)
            if item_doc_line:
                yield f'* `{item_name}()` - {item_doc_line}\n'

    module_names = extract.parse_specs(modules=modules)
    parts = []
    for module_name in sorted(module_names):
        module_obj = extract.load_module(module_name)
        pdoc_module = Module(module_obj)

        # Collect information

        module_doc_line = first_doc_line(pdoc_module.docstring)

        class_docs = list(get_doc_list(pdoc_list=pdoc_module.classes))
        func_docs = list(get_doc_list(pdoc_list=pdoc_module.functions))

        # Generate output only if information exists:

        if module_doc_line or class_docs or func_docs:
            level = module_name.count('.') + start_level
            parts.append(f'\n{"#" * level} {module_name}\n\n')
            # print(pdoc_module.source_file)

        if module_doc_line:
            parts.append(f'{module_doc_line}\n\n')

        parts.extend(class_docs)
        parts.extend(func_docs)
    return ''.join(parts)


def assert_readme(
    readme_path: Path,
    modules: list,
    start_marker_line: str = '[comment]: <> (✂✂✂ auto generated start ✂✂✂)',
    end_marker_line: str = '[comment]: <> (✂✂✂ auto generated end ✂✂✂)',
    start_level: int = 1,
):
    """
    Check and update README file with generate_modules_doc()
    The automatic generated documentation list will be "replace" between the given markers.
    """
    assert sys.version_info >= (3, 7), 'pdoc is not compatible with Python 3.6'

    assert readme_path.is_file()
    old_readme = readme_path.read_text()

    assert start_marker_line in old_readme
    assert end_marker_line in old_readme

    doc_block = generate_modules_doc(modules=modules, start_level=start_level)

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
