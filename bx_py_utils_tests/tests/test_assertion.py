import inspect
from unittest import TestCase

from bx_py_utils.test_utils.assertion import assert_equal, assert_text_equal, pformat_ndiff, text_ndiff


class AssertionTestCase(TestCase):
    def test_assert_equal(self):
        assert_equal(1, 1)
        assert_equal('a', 'a')
        x = object
        assert_equal(x, x)

        with self.assertRaises(AssertionError) as cm:
            assert_equal(1, 2, diff_func=pformat_ndiff)
        assert cm.exception.args[0] == 'Objects are not equal:\n- 1\n+ 2'

        with self.assertRaises(AssertionError) as cm:
            assert_equal(
                [{1: {2: 'two'}}],
                [{1: {2: 'XXX'}}]
            )
        assert cm.exception.args[0] == (
            'Objects are not equal:\n'
            '--- got\n'
            '\n'
            '+++ expected\n'
            '\n'
            '@@ -1,7 +1,7 @@\n'
            '\n'
            ' [\n'
            '     {\n'
            '         "1": {\n'
            '-            "2": "two"\n'
            '+            "2": "XXX"\n'
            '         }\n'
            '     }\n'
            ' ]'
        )

    def test_assert_text_equal(self):
        assert_text_equal(txt1='foo', txt2='foo')

        with self.assertRaises(AssertionError) as cm:
            assert_text_equal('1', '2', diff_func=text_ndiff)
        assert cm.exception.args[0] == 'Text not equal:\n- 1\n+ 2'

        with self.assertRaises(AssertionError) as cm:
            assert_text_equal(
                inspect.cleandoc('''
                    oNe
                    two
                    three
                    four
                    five
                '''),
                inspect.cleandoc('''
                    one
                    two
                    three
                    four
                    five
                '''),
            )
        assert cm.exception.args[0] == (
            'Text not equal:\n'
            '--- got\n'
            '\n'
            '+++ expected\n'
            '\n'
            '@@ -1,4 +1,4 @@\n'
            '\n'
            '-oNe\n'
            '+one\n'
            ' two\n'
            ' three\n'
            ' four'
        )
