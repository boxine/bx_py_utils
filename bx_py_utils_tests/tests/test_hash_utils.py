from unittest import TestCase

from bx_py_utils.dict_utils import DictCompareResult
from bx_py_utils.hash_utils import (
    collect_hashes,
    compare_hashes,
    url_safe_encode,
    url_safe_hash,
)


class HastUtilsTestCase(TestCase):
    def test_url_safe_encode(self):
        assert url_safe_encode(b'\x00\x01\x02\xfd\xfe\xff') == '-._GHJ'

    def test_url_safe_hash(self):
        assert url_safe_hash('foobar') == (
            'J45l_w.05QsjdV32~D-2hj-w2Jn8qL2FSkd2.vLhHZkGr-BmVrRpH-1LVgDJmMw_'
        )
        assert url_safe_hash('foobar', max_size=16) == ('J45l_w.05QsjdV32')

        with self.assertRaises(AssertionError) as cm:
            assert url_safe_hash('foobar', max_size=9999)
        assert cm.exception.args[0] == 'Hash digest too short for requested max size!'

    def test_collect_hashes(self):
        self.assertEqual(
            collect_hashes({'sha1': 'foo', 'other': 1, 'md5': 123, 'baz': None, 'sha224': None}),
            {'sha1': 'foo', 'md5': 123, 'sha224': None},
        )
        self.assertEqual(
            collect_hashes({1: 2, 'sha1': 'foo', 3: 4, 'file_size': 1}, extra_keys=('file_size',)),
            {'sha1': 'foo', 'file_size': 1},
        )

        # The extra key can be missing:
        self.assertEqual(
            collect_hashes({'foo': 1, 2: 3}, extra_keys=('foo', 'bar')),
            {'foo': 1},
        )

    def test_compare_hashes(self):
        # More deeper tests that also checks DictCompareResult.compare_successful()

        unrelated_data = {'foo': 'bar', 'baz': 'qux'}

        # All present hashes are equal -> successful
        result = compare_hashes(
            {'md5': '123', **unrelated_data},
            {'md5': '123', **unrelated_data},
        )
        self.assertEqual(
            result,
            DictCompareResult(correct_keys={'md5': '123'}, wrong_keys={}, skipped_keys={}),
        )
        self.assertIs(result.compare_successful(), True)

        # One hash different -> not successful
        result = compare_hashes(
            {'md5': '123', 'sha1': 'foo', **unrelated_data},
            {'md5': '123', 'sha1': 'bar', **unrelated_data},
        )
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={'md5': '123'},
                wrong_keys={'sha1': {'current': 'foo', 'expected': 'bar'}},
                skipped_keys={},
            ),
        )
        self.assertIs(result.compare_successful(), False)

        # No hashes to compare -> compare_successful() is None!
        result = compare_hashes(
            {'md5': '123', **unrelated_data},
            {'sha1': '123', **unrelated_data},
        )
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={},
                wrong_keys={},
                skipped_keys={
                    'md5': {'current': '123', 'expected': None},
                    'sha1': {'current': None, 'expected': '123'},
                },
            ),
        )
        self.assertIs(result.compare_successful(), None)

        # Use extra keys:
        result = compare_hashes(
            {'md5': '123', 'file_size': 456, **unrelated_data},
            {'md5': '123', 'file_size': 456, **unrelated_data},
            extra_keys=('file_size',),
        )
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={'md5': '123', 'file_size': 456},
                wrong_keys={},
                skipped_keys={},
            ),
        )
        self.assertIs(result.compare_successful(), True)

        # The extra key can be missing in one of the dicts:
        result = compare_hashes(
            {'md5': '123', 'file_size': 456, **unrelated_data},
            {'md5': '123', **unrelated_data},
            extra_keys=('file_size',),
        )
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={'md5': '123'},
                wrong_keys={},
                skipped_keys={'file_size': {'current': 456, 'expected': None}},
            ),
        )
        self.assertIs(result.compare_successful(), True)  # md5 matched

        # 0 on both sides are equal -> successful
        result = compare_hashes(
            {'file_size': 0, **unrelated_data},
            {'file_size': 0, **unrelated_data},
            extra_keys=('file_size',),
        )
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={'file_size': 0},
                wrong_keys={},
                skipped_keys={},
            ),
        )
        self.assertIs(result.compare_successful(), True)

        # Compare 0 with a non-zero value -> not successful
        result = compare_hashes(
            {'file_size': 123, **unrelated_data},
            {'file_size': 0, **unrelated_data},
            extra_keys=('file_size',),
        )
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={},
                wrong_keys={'file_size': {'current': 123, 'expected': 0}},
                skipped_keys={},
            ),
        )
        self.assertIs(result.compare_successful(), False)

        # We use a simple equality check: Different objects with the same value are equal!
        value1 = '9c7c7ec25d02d8925b1446dc96cb8d708a6790f000e668d545967635'
        # It's not easy to create string with the same value but different object id!
        # This works and forces a new string object:
        value2 = bytearray(value1, 'utf-8').decode('utf-8')

        # Isn't it really?
        self.assertEqual(value1, value2)
        self.assertNotEqual(id(value1), id(value2))

        # Ok, test it now:
        result = compare_hashes({'sha3_224': value1}, {'sha3_224': value2})
        self.assertEqual(
            result,
            DictCompareResult(
                correct_keys={'sha3_224': '9c7c7ec25d02d8925b1446dc96cb8d708a6790f000e668d545967635'},
                wrong_keys={},
                skipped_keys={},
            ),
        )
        self.assertIs(result.compare_successful(), True)
