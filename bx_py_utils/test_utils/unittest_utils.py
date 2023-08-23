import dataclasses
import doctest
import importlib
import inspect
import pkgutil
import pprint
import re
from pathlib import Path
from unittest import TestCase

from bx_py_utils.filename_matcher import filename_matcher
from bx_py_utils.path import assert_is_dir
from bx_py_utils.test_utils.redirect import RedirectOut


def assert_no_flat_tests_functions(path: Path):
    """
    Check if there exists normal test functions (That will not be executed by normal unittests)
    """
    assert_is_dir(path)

    errors = {}
    for item in path.rglob('test_*.py'):
        content = item.read_text(encoding='UTF-8')
        matches = re.findall(r'^def (test_.+):$', content, re.MULTILINE)
        if matches:
            errors[str(item.relative_to(path))] = matches

    if errors:
        raise AssertionError(f'Flat test files found:\n{pprint.pformat(errors)}')


@dataclasses.dataclass
class DocTestResults:
    passed: int = 0
    failed: int = 0
    skipped: int = 0


class BaseDocTests(TestCase):
    """
    Helper to include all doctests in unittests, without change unittest setup. Just add a normal TestCase.

    Just add this kind of code in your code base:

        from bx_py_utils.test_utils.unittest_utils import BaseDocTests

        class DocTests(BaseDocTests):
            def test_doctests(self):
                self.run_doctests(
                    modules=(foo1, bar2),  # Add your modules that should be scanned recursively for doctests
                    excludes=('**/settings', '**/migrations'),  # (Optional) exclude some file paths
                )
    """

    def run_doctests(
        self, modules: tuple, verbose=False, recurse=True, exclude_empty=True, excludes=None
    ) -> DocTestResults:
        results = DocTestResults()

        runner = doctest.DocTestRunner(verbose=verbose)
        finder = doctest.DocTestFinder(verbose=verbose, recurse=recurse, exclude_empty=exclude_empty)

        for module in modules:
            self.assertTrue(inspect.ismodule(module), f'Not a module: {module}')
            for info in pkgutil.walk_packages(module.__path__, module.__name__ + '.'):
                module_finder = info.module_finder
                module_path = module_finder.path
                if filename_matcher(patterns=excludes, file_path=module_path):
                    continue

                module = importlib.import_module(info.name)
                tests: list[doctest.DocTest] = finder.find(obj=module)
                for test in tests:
                    if excludes:
                        if filename_matcher(patterns=excludes, file_path=test.filename):
                            results.skipped += 1
                            with self.subTest(info.name):
                                self.skipTest(reason=f'Skip DocTest in: {test.filename}')
                            continue

                    with self.subTest(test.name):
                        with RedirectOut() as buffer:
                            result: doctest.TestResults = runner.run(test)
                        if result.failed:
                            results.failed += 1
                            self.fail(buffer.stdout)
                        else:
                            results.passed += 1

        return results
