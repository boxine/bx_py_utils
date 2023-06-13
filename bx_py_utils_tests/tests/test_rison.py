from unittest import TestCase

from bx_py_utils.rison import rison_dumps


class RISONTest(TestCase):
    def test_rison_dumps(self):
        self.assertEqual(rison_dumps(True), '!t')
        self.assertEqual(rison_dumps(False), '!f')
        self.assertEqual(rison_dumps(None), '!n')
        self.assertEqual(rison_dumps(None), '!n')
        self.assertEqual(rison_dumps(''), "''")
        self.assertEqual(rison_dumps('ab'), 'ab')  # no quoting necessary!
        self.assertEqual(rison_dumps('now-2d'), 'now-2d')  # no quoting here either!
        self.assertEqual(rison_dumps('.dot.'), '.dot.')  # even dots are fine
        self.assertEqual(rison_dumps('1.1'), "'1.1'")  # need to be escaped when including a number
        self.assertEqual(rison_dumps('a b'), '\'a b\'')
        self.assertEqual(
            rison_dumps('a\'b\\c"d!e!!f'), "'a!'b\\c\"d!!e!!!!f'"
        )  # only ' and ! need to be escaped
        self.assertEqual(rison_dumps([]), '!()')
        self.assertEqual(rison_dumps({'x': 1, 'y z': [2, 3]}), "('x':1,'y z':!(2,3))")

        # objects must be sorted
        self.assertEqual(rison_dumps({'ab': '2nd', 'ac': 'third', 'aa': 'first'}), "(aa:first,ab:'2nd',ac:third)")
