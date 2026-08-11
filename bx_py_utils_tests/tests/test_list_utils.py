from unittest import TestCase

from bx_py_utils.list_utils import dedupe_lines, unique_list


class ListUtilsTestCase(TestCase):
    def test_unique_list(self):
        self.assertEqual(unique_list([5, 1, 2, 5, 3, 2, 5, 4]), [5, 1, 2, 3, 4])

    def test_dedupe_lines(self):
        # empty
        self.assertEqual(list(dedupe_lines([])), [])
        # no duplicates
        self.assertEqual(list(dedupe_lines(['x', 'y', 'z'])), ['x', 'y', 'z'])
        # exactly 2: both kept, no cut marker
        self.assertEqual(list(dedupe_lines(['a', 'a'])), ['a', 'a'])
        # 3 in a row: no cut (list would not get shorter)
        self.assertEqual(list(dedupe_lines(['a', 'a', 'a'])), ['a', 'a', 'a'])
        # 4 in a row: first, cut 2, last
        self.assertEqual(
            list(dedupe_lines(['a', 'a', 'a', 'a'])),
            ['a', '...cut 2 lines...', 'a'],
        )
        # 5 in a row: first, cut 3, last
        self.assertEqual(
            list(dedupe_lines(['a', 'a', 'a', 'a', 'a'])),
            ['a', '...cut 3 lines...', 'a'],
        )
        # mixed: run of 3 passes through, later recurrence kept
        self.assertEqual(
            list(dedupe_lines(['a', 'a', 'a', 'b', 'c', 'b'])),
            ['a', 'a', 'a', 'b', 'c', 'b'],
        )
        # trailing run of 4: first, cut 2, last
        self.assertEqual(
            list(dedupe_lines(['a', 'b', 'b', 'b', 'b'])),
            ['a', 'b', '...cut 2 lines...', 'b'],
        )
        # multiple runs of 4 separated by single lines
        self.assertEqual(
            list(
                dedupe_lines(
                    [
                        'a',
                        'a',
                        'a',
                        'a',
                        'XXX',
                        'a',
                        'a',
                        'a',
                        'a',
                        'XXX',
                        'a',
                        'a',
                        'a',
                        'a',
                    ]
                )
            ),
            [
                'a',
                '...cut 2 lines...',
                'a',
                'XXX',
                'a',
                '...cut 2 lines...',
                'a',
                'XXX',
                'a',
                '...cut 2 lines...',
                'a',
            ],
        )
