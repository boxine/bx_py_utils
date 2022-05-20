# Boxine - bx_py_utils

Various Python utility functions


## Quickstart

```bash
pip install bx_py_utils
```


## Existing stuff

Here only a simple list about existing utilities.
Please take a look into the sources and tests for deeper informations.


[comment]: <> (✂✂✂ auto generated start ✂✂✂)

### bx_py_utils.anonymize

* [`anonymize()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/anonymize.py#L15-L43) - Anonymize the given string with special handling for eMail addresses.

### bx_py_utils.auto_doc

* [`assert_readme()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L121-L163) - Check and update README file with generate_modules_doc()
* [`generate_modules_doc()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L43-L118) - Generate a list of function/class information via pdoc.
* [`get_code_location()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L35-L40) - Return start and end line number for an object via inspect.

#### bx_py_utils.aws.client_side_cert_manager

* [`ClientSideCertManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/aws/client_side_cert_manager.py#L6-L72) - Helper to manage client-side TLS certificate via AWS Secrets Manager by

#### bx_py_utils.aws.secret_manager

* [`SecretsManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/aws/secret_manager.py#L4-L34) - Access AWS Secrets Manager values

### bx_py_utils.compat

* [`removeprefix()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/compat.py#L1-L7) - Backport of `removeprefix` from PEP-616 (Python 3.9+)
* [`removesuffix()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/compat.py#L10-L16) - Backport of `removesuffix` from PEP-616 (Python 3.9+)

### bx_py_utils.dict_utils

* [`dict_get()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/dict_utils.py#L4-L25) - nested dict `get()`
* [`pluck()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/dict_utils.py#L28-L40) - Extract values from a dict, if they are present

### bx_py_utils.environ

* [`cgroup_memory_usage()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/environ.py#L9-L25) - Returns the memory usage of the cgroup the Python interpreter is running in.

### bx_py_utils.error_handling

* [`print_exc_plus()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/error_handling.py#L14-L72) - Print traceback information with a listing of all the local variables in each frame.

### bx_py_utils.file_utils

* [`EmptyFileError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L16-L20) - Will be raised from get_and_assert_file_size() if a 0-bytes file was found.
* [`FileError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L8-L13) - Base error class for all 'file_utils' exceptions.
* [`FileHasher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L78-L103) - Context Manager for generate different hashes from file content while processing a file.
* [`FileSizeError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L23-L37) - File size is not the same as the expected size.
* [`NamedTemporaryFile2()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L52-L75) - Generates a temp file with the given filename **without** any random name sequence.
* [`TempFileHasher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L106-L165) - File like context manager that combines NamedTemporaryFile2 and FileHasher.
* [`get_and_assert_file_size()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/file_utils.py#L40-L49) - Check file size of given file object. Raise EmptyFileError for empty files or return size

### bx_py_utils.graphql_introspection

* [`introspection_query()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/graphql_introspection.py#L5-L25) - Generate GraphQL introspection query with variable nested depth.

### bx_py_utils.hash_utils

* [`url_safe_encode()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/hash_utils.py#L13-L22) - Encode bytes into a URL safe string.
* [`url_safe_hash()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/hash_utils.py#L25-L46) - Generate a URL safe hash with `max_size` from given string/bytes.

### bx_py_utils.html_utils

* [`ElementsNotFoundError()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L44-L48) - Happens if requested HTML elements cannot be found
* [`InvalidHtml()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L18-L41) - XMLSyntaxError with better error messages: used in validate_html()
* [`get_html_elements()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L97-L108) - Returns the selected HTML elements as string
* [`pretty_format_html()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L87-L94) - Pretty format given HTML document via BeautifulSoup (Needs 'beautifulsoup4' package)
* [`validate_html()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/html_utils.py#L51-L73) - Validate a HTML document via XMLParser (Needs 'lxml' package)

#### bx_py_utils.humanize.pformat

* [`pformat()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/humanize/pformat.py#L5-L16) - Format given object: Try JSON fist and fallback to pformat()

#### bx_py_utils.humanize.time

* [`human_timedelta()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/humanize/time.py#L14-L52) - Converts a time duration into a friendly text representation.

### bx_py_utils.iteration

* [`chunk_iterable()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/iteration.py#L4-L21) - Returns a generator that yields slices of iterable of the given `chunk_size`.

### bx_py_utils.path

* [`assert_is_dir()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L5-L13) - Check if given path is a directory
* [`assert_is_file()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L16-L26) - Check if given path is a file

### bx_py_utils.processify

* [`processify()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/processify.py#L12-L53) - Decorator to run a function as a process.

### bx_py_utils.stack_info

* [`FrameNotFound()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/stack_info.py#L8-L13) - Base class for lookup errors.
* [`last_frame_outside_path()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/stack_info.py#L16-L44) - Returns the stack frame that is the direct successor of given "file_path".

#### bx_py_utils.test_utils.assertion

* [`assert_equal()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L63-L76) - Check if the two objects are the same. Display a nice diff, using `pformat()`
* [`assert_text_equal()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L79-L94) - Check if the two text strings are the same. Display a error message with a diff.
* [`pformat_ndiff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L15-L25) - Generate a `ndiff` from two objects, using `pformat()`
* [`pformat_unified_diff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L46-L60) - Generate a unified diff from two objects, using `pformat()`
* [`text_ndiff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L7-L12) - Generate a `ndiff` between two text strings.
* [`text_unified_diff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L39-L43) - Generate a unified diff between two text strings.

#### bx_py_utils.test_utils.datetime

* [`parse_dt()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/datetime.py#L4-L15) - Helper for easy generate a `datetime` instance via string.

#### bx_py_utils.test_utils.filesystem_utils

* [`FileWatcher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/filesystem_utils.py#L6-L49) - Helper to record which new files have been created.

#### bx_py_utils.test_utils.log_utils

* [`RaiseLogUsage()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/log_utils.py#L4-L11) - A log handler, that raise an error on every log output.

#### bx_py_utils.test_utils.mock_aws_secret_manager

* [`SecretsManagerMock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_aws_secret_manager.py#L1-L16) - Mock for `bx_py_utils.aws.secret_manager.SecretsManager()`

#### bx_py_utils.test_utils.mock_boto3session

* [`MockedBoto3Session()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_boto3session.py#L4-L46) - Mock for `boto3.session.Session()`

#### bx_py_utils.test_utils.mock_uuid

* [`MockUUIDGenerator()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_uuid.py#L5-L25) - Helper to mock `uuid.uuid4()` with reproducible results (e.g. for snapshot tests)

#### bx_py_utils.test_utils.mocks3

A simple mock for Boto3's S3 modules.

* [`PseudoS3Client()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mocks3.py#L60-L209) - Simulates a boto3 S3 client object in tests

#### bx_py_utils.test_utils.requests_mock_assertion

* [`assert_json_requests_mock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L30-L45) - Check the requests mock history. In this case all requests must be JSON.
* [`assert_json_requests_mock_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L48-L55) - Check requests mock history via snapshot. Accepts only JSON requests.
* [`assert_requests_mock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L58-L78) - Check the requests mock history. Accept mixed "text" and "JSON".
* [`assert_requests_mock_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L81-L86) - Check requests mock history via snapshot. Accept mixed "text" and "JSON".

#### bx_py_utils.test_utils.snapshot

Assert complex output via auto updated snapshot files with nice diff error messages.

* [`assert_binary_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L303-L335) - Assert binary data via snapshot file
* [`assert_html_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L240-L287) - Assert "html" string via snapshot file with validate and pretty format
* [`assert_py_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L200-L237) - Assert complex python objects vio PrettyPrinter() snapshot file.
* [`assert_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L159-L197) - Assert given data serialized to JSON snapshot file.
* [`assert_text_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L120-L156) - Assert "text" string via snapshot file

#### bx_py_utils.test_utils.time

* [`MockTimeMonotonicGenerator()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/time.py#L1-L19) - Helper to mock `time.monotonic()` in tests.

### bx_py_utils.text_tools

* [`cutout()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/text_tools.py#L1-L36) - Mark a point in a long text by line no + column with context lines around.

[comment]: <> (✂✂✂ auto generated end ✂✂✂)


## Notes about snapshot

Quick hint about snapshot. If you have many snapshots in your project and you need to change many with a code change, then you can run the tests without a snapshot change leading to an error, by set `RAISE_SNAPSHOT_ERRORS=0` in your environment.

e.g.:

```bash
RAISE_SNAPSHOT_ERRORS=0 poetry run pytest
RAISE_SNAPSHOT_ERRORS=0 python3 -m unittest
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
help                 List all commands
install-poetry       install or update poetry
install              install via poetry
update               Update the dependencies as according to the pyproject.toml file
lint                 Run code formatters and linter
fix-code-style       Fix code formatting
tox-listenvs         List all tox test environments
tox                  Run pytest via tox with all environments
tox-py37             Run pytest via tox with *python v3.7*
tox-py38             Run pytest via tox with *python v3.8*
tox-py39             Run pytest via tox with *python v3.9*
tox-py310            Run pytest via tox with *python v3.10*
pytest               Run pytest
pytest-ci            Run pytest with CI settings
publish              Release new version to PyPi
clean                Remove created files from the test project
```


## License

[MIT](LICENSE). Patches welcome!

## About us

We’ve been rethinking the listening experience for kids and have created an ecosystem where haptic and listening experience are combined via smart technology - the Toniebox.

We are constantly looking for engineers to join our team in different areas. If you’d be interested in contributing to our platform, have a look at: https://tonies.com/jobs/

## Links

* https://pypi.org/project/bx-py-utils/
