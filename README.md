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

* [`anonymize()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/anonymize.py#L15) - Anonymize the given string with special handling for eMail addresses.

### bx_py_utils.auto_doc

* [`assert_readme()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L104) - Check and update README file with generate_modules_doc()
* [`generate_modules_doc()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/auto_doc.py#L34) - Generate a list of function/class information via pdoc.

#### bx_py_utils.aws.client_side_cert_manager

* [`ClientSideCertManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/aws/client_side_cert_manager.py#L6) - Helper to manage client-side TLS certificate via AWS Secrets Manager by

#### bx_py_utils.aws.secret_manager

* [`SecretsManager()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/aws/secret_manager.py#L4) - Access AWS Secrets Manager values

### bx_py_utils.compat

* [`removeprefix()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/compat.py#L1) - Backport of `removeprefix` from PEP-616 (Python 3.9+)
* [`removesuffix()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/compat.py#L10) - Backport of `removesuffix` from PEP-616 (Python 3.9+)

### bx_py_utils.dict_utils

* [`dict_get()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/dict_utils.py#L4) - nested dict `get()`
* [`pluck()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/dict_utils.py#L28) - Extract values from a dict, if they are present

### bx_py_utils.environ

* [`cgroup_memory_usage()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/environ.py#L9) - Returns the memory usage of the cgroup the Python interpreter is running in.

### bx_py_utils.error_handling

* [`print_exc_plus()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/error_handling.py#L14) - Print traceback information with a listing of all the local variables in each frame.

### bx_py_utils.graphql_introspection

* [`introspection_query()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/graphql_introspection.py#L5) - Generate GraphQL introspection query with variable nested depth.

### bx_py_utils.hash_utils

* [`url_safe_encode()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/hash_utils.py#L13) - Encode bytes into a URL safe string.
* [`url_safe_hash()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/hash_utils.py#L25) - Generate a URL safe hash with `max_size` from given string/bytes.

#### bx_py_utils.humanize.pformat

* [`pformat()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/humanize/pformat.py#L5) - Format given object: Try JSON fist and fallback to pformat()

#### bx_py_utils.humanize.time

* [`human_timedelta()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/humanize/time.py#L14) - Converts a time duration into a friendly text representation.

### bx_py_utils.iteration

* [`chunk_iterable()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/iteration.py#L4) - Returns a generator that yields slices of iterable of the given `chunk_size`.

### bx_py_utils.path

* [`assert_is_dir()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L4) - Check if given path is a directory
* [`assert_is_file()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/path.py#L15) - Check if given path is a file

### bx_py_utils.processify

* [`processify()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/processify.py#L12) - Decorator to run a function as a process.

### bx_py_utils.stack_info

* [`FrameNotFound()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/stack_info.py#L8) - Base class for lookup errors.
* [`last_frame_outside_path()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/stack_info.py#L16) - Returns the stack frame that is the direct successor of given "file_path".

#### bx_py_utils.test_utils.assertion

* [`assert_equal()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L52) - Check if the two objects are the same. Display a nice diff, using `pformat()`
* [`assert_text_equal()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L68) - Check if the two text strings are the same. Display a error message with a diff.
* [`pformat_ndiff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L14) - Generate a `ndiff` from two objects, using `pformat()`
* [`pformat_unified_diff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L45) - Generate a unified diff from two objects, using `pformat()`
* [`text_ndiff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L6) - Generate a `ndiff` between two text strings.
* [`text_unified_diff()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/assertion.py#L38) - Generate a unified diff between two text strings.

#### bx_py_utils.test_utils.datetime

* [`parse_dt()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/datetime.py#L4) - Helper for easy generate a `datetime` instance via string.

#### bx_py_utils.test_utils.filesystem_utils

* [`FileWatcher()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/filesystem_utils.py#L6) - Helper to record which new files have been created.

#### bx_py_utils.test_utils.mock_aws_secret_manager

* [`SecretsManagerMock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_aws_secret_manager.py#L1) - Mock for `bx_py_utils.aws.secret_manager.SecretsManager()`

#### bx_py_utils.test_utils.mock_boto3session

* [`MockedBoto3Session()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/mock_boto3session.py#L4) - Mock for `boto3.session.Session()`

#### bx_py_utils.test_utils.requests_mock_assertion

* [`assert_json_requests_mock()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/requests_mock_assertion.py#L6) - Check the requests history.

#### bx_py_utils.test_utils.snapshot

Assert complex output via auto updated snapshot files with nice diff error messages.

* [`assert_py_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L166) - Assert complex python objects vio PrettyPrinter() snapshot file.
* [`assert_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L132) - Assert given data serialized to JSON snapshot file.
* [`assert_text_snapshot()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/snapshot.py#L99) - Assert "text" string via snapshot file

#### bx_py_utils.test_utils.time

* [`MockTimeMonotonicGenerator()`](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/test_utils/time.py#L1) - Helper to mock `time.monotonic()` in tests.

[comment]: <> (✂✂✂ auto generated end ✂✂✂)


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
tox-py36             Run pytest via tox with *python v3.6*
tox-py37             Run pytest via tox with *python v3.7*
tox-py38             Run pytest via tox with *python v3.8*
tox-py39             Run pytest via tox with *python v3.9*
pytest               Run pytest
pytest-ci            Run pytest with CI settings
publish              Release new version to PyPi
clean                Remove created files from the test project
```


## License

[MIT](LICENSE). Patches welcome!

## Links

* https://pypi.org/project/bx-py-utils/
