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
        self.assertEqual(rison_dumps('a b'), '\'a b\'')
        self.assertEqual(
            rison_dumps('a\'b\\c"d!e!!f'), "'a!'b\\c\"d!!e!!!!f'"
        )  # only ' and ! need to be escaped
        self.assertEqual(rison_dumps([]), '!()')
        self.assertEqual(rison_dumps({'x': 1, 'y z': [2, 3]}), "('x':1,'y z':!(2,3))")
