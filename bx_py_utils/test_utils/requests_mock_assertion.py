from json import JSONDecodeError
from pathlib import Path

from bx_py_utils.test_utils.assertion import assert_equal
from bx_py_utils.test_utils.snapshot import assert_snapshot


def build_requests_mock_history(mock, only_json=True):
    history = []
    for request in mock.request_history:

        request_info = {
            'request': f'{request.method} {request.url}'
        }
        try:
            json_data = request.json()
        except JSONDecodeError as err:
            if only_json:
                raise AssertionError(
                    f'{request.method} {request.url} without valid JSON: {err} in:\n{err.doc!r}'
                )
            request_info['text'] = request.text
        else:
            request_info['json'] = json_data

        history.append(request_info)
    return history


def assert_json_requests_mock(mock, data):
    """
    Check the requests mock history. In this case all requests must be JSON.
    e.g.:

        with requests_mock.mock() as m:
            m.post('http://test.tld', text='resp')
            requests.post('http://test.tld', json={'foo': 'bar'})

        assert_json_requests_mock(mock=m, data=[{
            'request': 'POST http://test.tld/',
            'json': {'foo': 'bar'},
        }])
    """
    history = build_requests_mock_history(mock, only_json=True)
    assert_equal(history, data, msg='Request history are not equal:')


def assert_json_requests_mock_snapshot(mock):
    """
    Check requests mock history via snapshot. Accepts only JSON requests.
    :param mock:
    :return:
    """
    history = build_requests_mock_history(mock, only_json=True)
    assert_snapshot(got=history, self_file_path=Path(__file__))


def assert_requests_mock(mock, data):
    """
    Check the requests mock history. Accept mixed "text" and "JSON".
    e.g.:

        with requests_mock.mock() as m:
            m.get('http://test.tld', text='foo')
            m.post('http://test.tld', text='bar')
            requests.post('http://test.tld', data={'foo': 'one'})
            requests.post('http://test.tld', json={'foo': 'two'})

        assert_requests_mock(mock=m, data=[{
            'request': 'POST http://test.tld/',
            'text': 'foo=one',
        }, {
            'request': 'POST http://test.tld/',
            'json': {'foo': 'two'},
        }])
    """
    history = build_requests_mock_history(mock, only_json=False)
    assert_equal(history, data, msg='Request history are not equal:')


def assert_requests_mock_snapshot(mock):
    """
    Check requests mock history via snapshot. Accept mixed "text" and "JSON".
    """
    history = build_requests_mock_history(mock, only_json=False)
    assert_snapshot(got=history, self_file_path=Path(__file__))
