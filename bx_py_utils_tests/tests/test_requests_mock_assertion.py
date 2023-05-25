from unittest import TestCase

import requests
import requests_mock

from bx_py_utils.test_utils.requests_mock_assertion import (
    assert_json_requests_mock,
    assert_json_requests_mock_snapshot,
    assert_requests_mock,
    assert_requests_mock_snapshot,
)


class RequestsMockAssertionTestCase(TestCase):
    def test_basic_assert_json_requests_mock(self):
        with requests_mock.mock() as m:
            m.post('http://test.tld', text='resp')
            requests.post('http://test.tld', json={'foo': 'bar'})

        assert_json_requests_mock(mock=m, data=[{
            'request': 'POST http://test.tld/',
            'json': {'foo': 'bar'},
        }])

    def test_basic_assert_requests_mock(self):
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

    def test_no_valid_json(self):
        with requests_mock.mock() as m:
            m.post('http://test.tld', text='resp')
            requests.post('http://test.tld', data='This it no JSON !')

        with self.assertRaises(AssertionError) as cm:
            assert_json_requests_mock(mock=m, data=[{
                'request': 'POST https://foo.tld/bar/',
                'json': {'req': 'one'},
            }])
        assert cm.exception.args[0] == (
            "POST http://test.tld/ without valid JSON:"
            " Expecting value: line 1 column 1 (char 0) in:\n"
            "'This it no JSON !'"
        )

    def test(self):
        with requests_mock.mock() as m:
            m.post(
                'https://foo.tld/bar/',
                response_list=[
                    {'json': {'info': '1'}, },
                    {'json': {'info': '2'}, },
                ]
            )
            requests.post(
                url='https://foo.tld/bar/',
                json={'req': 'one'}
            )
            requests.post(
                url='https://foo.tld/bar/',
                json={'req': 'two'}
            )

        assert_json_requests_mock(mock=m, data=[{
            'request': 'POST https://foo.tld/bar/',
            'json': {'req': 'one'},
        }, {
            'request': 'POST https://foo.tld/bar/',
            'json': {'req': 'two'},
        }])

        with self.assertRaises(AssertionError) as cm:
            assert_json_requests_mock(mock=m, data=[{
                'request': 'POST https://foo.tld/bar/',
                'json': {'req': 'one'},
            }, {
                'request': 'POST https://foo.tld/bar/',
                'json': {'req': 'XXX'},
            }])
        assert cm.exception.args[0] == (
            'Request history are not equal:\n'
            '--- got\n'
            '\n'
            '+++ expected\n'
            '\n'
            '@@ -7,7 +7,7 @@\n'
            '\n'
            '     },\n'
            '     {\n'
            '         "json": {\n'
            '-            "req": "two"\n'
            '+            "req": "XXX"\n'
            '         },\n'
            '         "request": "POST https://foo.tld/bar/"\n'
            '     }'
        )

    def test_assert_json_requests_mock_snapshot(self):
        with requests_mock.mock() as m:
            m.post('http://test.tld', text='resp')
            requests.post('http://test.tld', json={'foo': 'bar'})

        assert_json_requests_mock_snapshot(mock=m)

    def test_assert_requests_mock_snapshot(self):
        with requests_mock.mock() as m:
            m.get('http://test.tld', text='foo')
            m.post('http://test.tld', text='bar')
            requests.post('http://test.tld', data={'foo': 'one'})
            requests.post('http://test.tld', json={'foo': 'two'})

        assert_requests_mock_snapshot(mock=m)

    def test_assert_json_requests_mock_with_none(self):
        with requests_mock.mock() as m:
            m.get('http://test.tld')
            requests.get('http://test.tld')

        assert_json_requests_mock(mock=m, data=[{'request': 'GET http://test.tld/'}])
