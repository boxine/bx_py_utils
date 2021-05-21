# Boxine - bx_py_utils

Various Python utility functions


## Quickstart

```bash
pip install bx_py_utils
```


## Existing stuff

Here only a simple list about existing utilities.
Please take a look into the sources and tests for deeper informations.


### test utilities

* `datetime.parse_dt()` - Handy `datetime.strptime()` convert
* `assert_json_requests_mock()` - Check the requests history of `requests_mock.mock()`
* `assert_equal()` - Compare objects with a nice diff using pformat
* `assert_text_equal()` - Compare text strings with a nice diff
* `assert_snapshot` - Helper for quick snapshot test functionality (comparing value with one stored in a file using json)
* `assert_text_snapshot` - Same as `assert_snapshot` comparing text strings
* `assert_py_snapshot` - Snapshot test using `PrettyPrinter()`

### humanize

* `humanize.time.human_timedelta()` - Converts a time duration into a friendly text representation. (`X ms`, `sec`, `minutes` etc.)
* `pformat()` - Better `pretty-print-format` using JSON with fallback to `pprint.pformat()`


### AWS stuff

* `bx_py_utils.aws.secret_manager.SecretsManager` - Get values from AWS Secrets Manager
* `bx_py_utils.test_utils.mock_aws_secret_manager.SecretsManagerMock` - Mock our `SecretsManager()` helper in tests
* `bx_py_utils.test_utils.mock_boto3session.MockedBoto3Session` - Mock `boto3.session.Session()` (Currently only `get_secret_value()`)
* `bx_py_utils.aws.client_side_cert_manager.ClientSideCertManager` - Helper to manage client-side TLS certificate via AWS Secrets Manager

### GraphQL

* `graphql_introspection.introspection_query` Generate an introspection query to get an introspection doc.
* `graphql_introspection.complete_query` Generate a full query for all fields from an introspection doc.

### misc

* `dict_utils.dict_get()` - nested dict `get()`
* `dict_utils.pluck()` - Extract values from a dict, if they are present
* `environ.cgroup_memory_usage()` - Get the memory usage of the current cgroup
* `error_handling.print_exc_plus()` - Print traceback information with a listing of all the local variables in each frame
* `iteration.chunk_iterable()` - Create chunks off of any iterable
* `processify.processify()` - Will execute the decorated function in a separate process
* `anonymize.anonymize()` - Anonymize a string (With special handling of email addresses)
* `hash_utils.url_safe_hash()` - Generate URL safe hashes
* `compat.removeprefix()` - Backport of `str.removeprefix` from PEP-616
* `compat.removesuffix()` - Backport of `str.removesuffix` from PEP-616


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
