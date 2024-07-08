# Boxine - bx_py_utils

Various Python utility functions

[![tests](https://github.com/boxine/bx_py_utils/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/boxine/bx_py_utils/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/boxine/bx_py_utils/branch/master/graph/badge.svg)](https://app.codecov.io/github/boxine/bx_py_utils)
[![bx_py_utils @ PyPi](https://img.shields.io/pypi/v/bx_py_utils?label=bx_py_utils%20%40%20PyPi)](https://pypi.org/project/bx_py_utils/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bx_py_utils)](https://github.com/boxine/bx_py_utils/blob/master/pyproject.toml)
[![License MIT](https://img.shields.io/pypi/l/bx_py_utils)](https://github.com/boxine/bx_py_utils/blob/master/LICENSE)


## Quickstart

```bash
pip install bx_py_utils
```


## Existing stuff

Here only a simple list about existing utilities.
Please take a look into the sources and tests for deeper informations.


[comment]: <> (✂✂✂ auto generated start ✂✂✂)

### bx_py_utils.anonymize

* [`anonymize()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/anonymize.py#L15-L38) - Anonymize the given string with special handling for eMail addresses.

### bx_py_utils.auto_doc

* [`FnmatchExclude()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L203-L212) - Helper for auto doc `exclude_func` that exclude files via fnmatch pattern.
* [`assert_readme()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L174-L200) - Check and update README file with generate_modules_doc()
* [`assert_readme_block()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L141-L171) - Check and update README file: Asset that "text_block" is present between the markers.
* [`generate_modules_doc()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L46-L138) - Generate a list of function/class information via pdoc.
* [`get_code_location()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L38-L43) - Return start and end line number for an object via inspect.

#### bx_py_utils.aws.client_side_cert_manager

* [`ClientSideCertManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/aws/client_side_cert_manager.py#L6-L72) - Helper to manage client-side TLS certificate via AWS Secrets Manager by

#### bx_py_utils.aws.secret_manager

* [`SecretsManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/aws/secret_manager.py#L4-L34) - Access AWS Secrets Manager values

### bx_py_utils.compat

* [`removeprefix()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/compat.py#L1-L7) - Backport of `removeprefix` from PEP-616 (Python 3.9+)
* [`removesuffix()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/compat.py#L10-L16) - Backport of `removesuffix` from PEP-616 (Python 3.9+)

### bx_py_utils.dict_utils

* [`dict_get()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/dict_utils.py#L6-L27) - nested dict `get()`
* [`pluck()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/dict_utils.py#L30-L42) - Extract values from a dict, if they are present

### bx_py_utils.doc_write

Doc-Write, see: https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/doc_write/README.md


### bx_py_utils.environ

* [`OverrideEnviron()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/environ.py#L31-L54) - Context manager to change 'os.environ' temporarily.
* [`cgroup_memory_usage()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/environ.py#L12-L28) - Returns the memory usage of the cgroup the Python interpreter is running in.

### bx_py_utils.error_handling

* [`print_exc_plus()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/error_handling.py#L14-L72) - Print traceback information with a listing of all the local variables in each frame.

### bx_py_utils.file_utils

* [`EmptyFileError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L18-L21) - Will be raised from get_and_assert_file_size() if a 0-bytes file was found.
* [`FileError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L12-L15) - Base error class for all 'file_utils' exceptions.
* [`FileHasher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L79-L104) - Context Manager for generate different hashes from file content while processing a file.
* [`FileSizeError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L24-L38) - File size is not the same as the expected size.
* [`NamedTemporaryFile2()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L53-L76) - Generates a temp file with the given filename **without** any random name sequence.
* [`OverlongFilenameError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L188-L191) - cut_filename() error: The file name can not be shortened, because sterm is to short.
* [`TempFileHasher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L107-L178) - File like context manager that combines NamedTemporaryFile2 and FileHasher.
* [`cut_filename()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L194-L234) - Short the file name (and keep the last suffix). Raise OverlongFilenameError if it can't fit.
* [`get_and_assert_file_size()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L41-L50) - Check file size of given file object. Raise EmptyFileError for empty files or return size
* [`safe_filename()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L181-L185) - Makes an arbitrary input suitable to be used as a filename.

### bx_py_utils.filename_matcher

* [`filename_matcher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/filename_matcher.py#L6-L25) - Enhance fnmatch that accept a list of patterns.

### bx_py_utils.graphql_introspection

* [`introspection_query()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/graphql_introspection.py#L5-L25) - Generate GraphQL introspection query with variable nested depth.

### bx_py_utils.hash_utils

* [`url_safe_encode()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/hash_utils.py#L13-L22) - Encode bytes into a URL safe string.
* [`url_safe_hash()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/hash_utils.py#L25-L46) - Generate a URL safe hash with `max_size` from given string/bytes.

### bx_py_utils.html_utils

* [`ElementsNotFoundError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L44-L48) - Happens if requested HTML elements cannot be found
* [`InvalidHtml()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L18-L41) - XMLSyntaxError with better error messages: used in validate_html()
* [`get_html_elements()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L95-L106) - Returns the selected HTML elements as string
* [`pretty_format_html()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L87-L92) - Pretty format given HTML document via BeautifulSoup (Needs 'beautifulsoup4' package)
* [`validate_html()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L51-L73) - Validate a HTML document via XMLParser (Needs 'lxml' package)

#### bx_py_utils.humanize.pformat

* [`pformat()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/humanize/pformat.py#L5-L16) - Format given object: Try JSON fist and fallback to pformat()

#### bx_py_utils.humanize.time

* [`human_timedelta()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/humanize/time.py#L14-L52) - Converts a time duration into a friendly text representation.

### bx_py_utils.iteration

* [`chunk_iterable()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/iteration.py#L4-L21) - Returns a generator that yields slices of iterable of the given `chunk_size`.

### bx_py_utils.path

* [`ChangeCurrentWorkDir()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L39-L54) - Context Manager change the "CWD" to an other directory.
* [`MockCurrentWorkDir()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L57-L76) - Context Manager to move the "CWD" to a temp directory.
* [`assert_is_dir()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L7-L15) - Check if given path is a directory
* [`assert_is_file()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L18-L28) - Check if given path is a file

### bx_py_utils.processify

* [`processify()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/processify.py#L12-L53) - Decorator to run a function as a process.

### bx_py_utils.pyproject_toml

* [`get_pyproject_config()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/pyproject_toml.py#L17-L41) - Get a config section from "pyproject.toml". The path can be optional specify.

### bx_py_utils.rison

* [`rison_dumps()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/rison.py#L4-L31) - Encode as RISON, a URL-safe encoding format.

### bx_py_utils.stack_info

* [`FrameNotFound()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/stack_info.py#L8-L13) - Base class for lookup errors.
* [`last_frame_outside_path()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/stack_info.py#L16-L44) - Returns the stack frame that is the direct successor of given "file_path".

### bx_py_utils.string_utils

* [`compare_sentences()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/string_utils.py#L68-L89) - Calculates the Levenshtein distance between text1 and text2. With filter functionality.
* [`ensure_lf()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/string_utils.py#L105-L115) - Replace line endings to unix-style.
* [`get_words()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/string_utils.py#L41-L65) - Extract words from a text. With filter functionality.
* [`levenshtein_distance()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/string_utils.py#L9-L38) - Calculates the Levenshtein distance between two strings.
* [`startswith_prefixes()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/string_utils.py#L118-L134) - >>> startswith_prefixes('foobar', prefixes=('foo','bar'))
* [`uuid_from_text()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/string_utils.py#L92-L102) - Generate a UUID instance from the given text in a determinism may via SHA224 hash.

#### bx_py_utils.test_utils.assertion

* [`assert_equal()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L64-L77) - Check if the two objects are the same. Display a nice diff, using `pformat()`
* [`assert_text_equal()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L80-L95) - Check if the two text strings are the same. Display an error message with a diff.
* [`pformat_ndiff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L16-L26) - Generate a `ndiff` from two objects, using `pformat()`
* [`pformat_unified_diff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L47-L61) - Generate a unified diff from two objects, using `pformat()`
* [`text_ndiff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L8-L13) - Generate a `ndiff` between two text strings.
* [`text_unified_diff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L40-L44) - Generate a unified diff between two text strings.

#### bx_py_utils.test_utils.context_managers

* [`MassContextManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/context_managers.py#L1-L23) - A context manager that enter/exit a list of mocks.

#### bx_py_utils.test_utils.datetime

* [`parse_dt()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/datetime.py#L4-L15) - Helper for easy generate a `datetime` instance via string.

#### bx_py_utils.test_utils.deny_requests

* [`DenyAnyRealRequestContextManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/deny_requests.py#L24-L38) - Context manager that denies any request via docket/urllib3. Will raise DenyCallError.
* [`deny_any_real_request()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/deny_requests.py#L41-L50) - Deny any request via docket/urllib3. Useful for tests, because they should mock all requests.

#### bx_py_utils.test_utils.filesystem_utils

* [`FileWatcher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/filesystem_utils.py#L6-L49) - Helper to record which new files have been created.

#### bx_py_utils.test_utils.log_utils

* [`NoLogs()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/log_utils.py#L14-L31) - Context manager to Suppress all logger outputs
* [`RaiseLogUsage()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/log_utils.py#L4-L11) - A log handler, that raise an error on every log output.

#### bx_py_utils.test_utils.mock_aws_secret_manager

* [`SecretsManagerMock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_aws_secret_manager.py#L1-L16) - Mock for `bx_py_utils.aws.secret_manager.SecretsManager()`

#### bx_py_utils.test_utils.mock_boto3session

* [`MockedBoto3Session()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_boto3session.py#L4-L46) - Mock for `boto3.session.Session()`

#### bx_py_utils.test_utils.mock_uuid

* [`MockUUIDGenerator()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_uuid.py#L5-L25) - Helper to mock `uuid.uuid4()` with reproducible results (e.g. for snapshot tests)

#### bx_py_utils.test_utils.mocks3

A simple mock for Boto3's S3 modules.

* [`PseudoS3Client()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mocks3.py#L60-L246) - Simulates a boto3 S3 client object in tests

#### bx_py_utils.test_utils.redirect

* [`RedirectOut()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/redirect.py#L7-L34) - Redirect stdout + stderr into a buffer (with optional strip the output)

#### bx_py_utils.test_utils.requests_mock_assertion

* [`assert_json_requests_mock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L29-L44) - Check the requests mock history. In this case all requests must be JSON.
* [`assert_json_requests_mock_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L47-L54) - Check requests mock history via snapshot. Accepts only JSON requests.
* [`assert_requests_mock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L57-L77) - Check the requests mock history. Accept mixed "text" and "JSON".
* [`assert_requests_mock_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L80-L85) - Check requests mock history via snapshot. Accept mixed "text" and "JSON".

#### bx_py_utils.test_utils.snapshot

Assert complex output via auto updated snapshot files with nice diff error messages.

* [`SnapshotChanged()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L50-L51) - Assertion failed.
* [`assert_binary_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L366-L407) - Assert binary data via snapshot file
* [`assert_html_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L301-L350) - Assert "html" string via snapshot file with validate and pretty format
* [`assert_py_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L252-L298) - Assert complex python objects vio PrettyPrinter() snapshot file.
* [`assert_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L202-L249) - Assert given data serialized to JSON snapshot file.
* [`assert_text_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L154-L199) - Assert "text" string via snapshot file
* [`get_snapshot_file()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L124-L151) - Generate a file path use stack information to fill not provided path components.

#### bx_py_utils.test_utils.time

* [`MockTimeMonotonicGenerator()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/time.py#L1-L19) - Helper to mock `time.monotonic()` in tests.

#### bx_py_utils.test_utils.unittest_utils

* [`BaseDocTests()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/unittest_utils.py#L40-L91) - Helper to include all doctests in unittests, without change unittest setup. Just add a normal TestCase.
* [`assert_no_flat_tests_functions()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/unittest_utils.py#L16-L30) - Check if there exists normal test functions (That will not be executed by normal unittests)

### bx_py_utils.text_tools

* [`cutout()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/text_tools.py#L1-L36) - Mark a point in a long text by line no + column with context lines around.

[comment]: <> (✂✂✂ auto generated end ✂✂✂)


## Notes about snapshot

Quick hint about snapshot. If you have many snapshots in your project and you need to change many with a code change, then you can run the tests without a snapshot change leading to an error, by set `RAISE_SNAPSHOT_ERRORS=0` in your environment.

e.g.:

```bash
RAISE_SNAPSHOT_ERRORS=0 python3 -m unittest
```

Renew all snapshot files with:
```bash
make update-test-snapshot-files
```

## Backwards-incompatible changes

### v36 -> v37 - Outsourcing Django stuff

We split `bx_py_utils` and moved all Django related utilities into the separated project:

* https://github.com/boxine/bx_django_utils

So, `bx_py_utils` is better usable in non-Django projects, because Django will not installed as decency of "bx_py_utils"


## developing

To start developing e.g.:

```bash
~$ git clone https://github.com/boxine/bx_py_utils.git
~$ cd bx_py_utils
~/bx_py_utils$ make
help                       List all commands
install-base-req           Install needed base packages via apt
install                    Install the project in a Python virtualenv
update-requirements        Update requirements
lint                       Run code formatters and linter
fix-code-style             Fix code formatting
tox-listenvs               List all tox test environments
tox                        Run tests via tox with all environments
test                       Run tests
coverage                   Run tests with coverage
update-test-snapshot-files Update all snapshot files (by remove and recreate all snapshot files)
mypy                       Run mypy
safety                     Run https://github.com/pyupio/safety
publish                    Release new version to PyPi
clean                      Remove created files from the test project
```


## Create a release

* Increase verion number in `bx_py_utils/__init__.py`
* Create pull request
* After merge, call: `make publish`


## License

[MIT](LICENSE). Patches welcome!

## About us

We’ve been rethinking the listening experience for kids and have created an ecosystem where haptic and listening experience are combined via smart technology - the Toniebox.

We are constantly looking for engineers to join our team in different areas. If you’d be interested in contributing to our platform, have a look at: https://tonies.com/jobs/

## Links

* https://pypi.org/project/bx-py-utils/
