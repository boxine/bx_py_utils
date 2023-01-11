from unittest import TestCase
from uuid import UUID

from bx_py_utils.string_utils import compare_sentences, ensure_lf, get_words, levenshtein_distance, uuid_from_text


class StringUtilsTestCase(TestCase):
    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance('planet', 'planetary'), 3)
        self.assertEqual(levenshtein_distance('', 'test'), 4)
        self.assertEqual(levenshtein_distance('book', 'back'), 2)
        self.assertEqual(levenshtein_distance('book', 'book'), 0)
        self.assertEqual(levenshtein_distance('test', ''), 4)
        self.assertEqual(levenshtein_distance('', ''), 0)
        self.assertEqual(levenshtein_distance('orchestration', 'container'), 10)

    def test_get_words(self):
        self.assertEqual(get_words('One, two!'), ['one', 'two'])
        self.assertEqual(get_words("It's okay!"), ['its', 'okay'])
        self.assertEqual(get_words('test Äöüß!'), ['test', 'äöüß'])
        self.assertEqual(get_words('12 123 1234', min_word_length=3), ['123', '1234'])
        self.assertEqual(
            get_words('A AB cd EfG hij', min_word_length=2, ignore_words=('ab', 'efg')),
            ['cd', 'hij'],
        )

    def test_compare_sentences(self):
        self.assertEqual(compare_sentences('planet', 'planetary'), 3)
        self.assertEqual(compare_sentences('orchestration', 'container'), 10)

        self.assertEqual(compare_sentences('This is the SAME!', 'this is the same'), 0)

        # If "min_word_length" and "ignore_words" filters the complete content,
        # then we get None back:
        self.assertIsNone(compare_sentences('1', '2', min_word_length=2))
        self.assertIsNone(compare_sentences('1', '2', ignore_words=('1',)))
        self.assertIsNone(compare_sentences('1', '2', ignore_words=('2',)))

        # But if both text parts are exactly the same
        # then "min_word_length" and "ignore_words" will be ignored:
        self.assertEqual(
            compare_sentences(
                text1='the same foo bar',
                text2='the same foo bar',
                min_word_length=999,
                ignore_words=('the same', 'foo', 'bar'),
            ),
            0,
        )

    def test_uuid_from_text(self):
        self.assertEqual(uuid_from_text('foo'), UUID('0808f64e-60d5-8979-fcb6-76c96ec93827'))
        self.assertEqual(uuid_from_text('foo'), UUID('0808f64e-60d5-8979-fcb6-76c96ec93827'))
        self.assertEqual(uuid_from_text('bar'), UUID('07daf010-de7f-7f0d-8d76-a76eb8d1eb40'))

    def test_ensure_lf(self):
        self.assertEqual(ensure_lf('foo\r\nbar'), 'foo\nbar')
        self.assertEqual(ensure_lf('foo\rbar'), 'foo\nbar')
        self.assertEqual(ensure_lf('foo\r\rbar'), 'foo\n\nbar')
        self.assertEqual(ensure_lf('foo\r\n\r\rbar'), 'foo\n\n\nbar')
        self.assertEqual(ensure_lf(''), '')

        # None is also accepted and just pass:
        self.assertEqual(ensure_lf(None), None)
