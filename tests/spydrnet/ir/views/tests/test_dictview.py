import unittest
from spydrnet.ir.views.dictview import DictView

class TestDictView(unittest.TestCase):
    def setUp(self) -> None:
        self.dict_1 = dict(map(lambda x: (x, str(x)), range(10)))
        self.dict_2 = dict(map(lambda x: (x, str(x)), range(10, 20)))
        self.dict_view_1 = DictView(self.dict_1)
        self.dict_view_2 = DictView(self.dict_2)
        self.dict_3 = dict(map(lambda x: (x, str(x)), range(30, 30)))

    def test_eq(self):
        self.assertEqual(self.dict_view_1, self.dict_1)
        self.assertEqual(self.dict_1, self.dict_view_1)
        self.assertEqual(DictView(self.dict_1), self.dict_view_1)
        self.assertFalse(DictView(self.dict_2) == self.dict_view_1)

    def test_hash(self):
        self.assertRaises(TypeError, hash, self.dict_view_1)

    def test_len(self):
        self.assertEqual(len(self.dict_1), len(self.dict_view_1))

    def test_ne(self):
        self.assertNotEqual(self.dict_view_2, self.dict_1)
        self.assertNotEqual(self.dict_2, self.dict_view_1)
        self.assertNotEqual(DictView(self.dict_2), self.dict_view_1)
        self.assertTrue(DictView(self.dict_2) != self.dict_view_1)

    def test_repr(self):
        self.assertEqual(repr(self.dict_view_1), repr(self.dict_1))

    def test_str(self):
        self.assertEqual(str(self.dict_view_1), str(self.dict_1))

    def test_contains(self):
        self.assertTrue(5 in self.dict_view_1)
        self.assertFalse(10 in self.dict_view_1)

    def test_getitem(self):
        for ii in range(10):
            self.assertTrue(self.dict_view_1[ii] == str(ii))

    def test_iter(self):
        for ii, jj in zip(self.dict_view_1, range(10)):
            self.assertEqual(ii, jj)

    def test_get(self):
        for ii in range(11):
            self.assertTrue(self.dict_view_1.get(ii, '10') == str(ii))

    def test_copy(self):
        self.assertEqual(dict(map(lambda x: (x, str(x)), range(10))), self.dict_view_1.copy())

    def test_fromkeys(self):
        self.assertEqual(self.dict_view_1.fromkeys(range(10), 5), dict(map(lambda x: (x, 5), range(10))))

    def test_keys(self):
        for ii, jj in zip(self.dict_view_1.keys(), range(10)):
            self.assertEqual(ii, jj)

    def test_values(self):
        for ii, jj in zip(self.dict_view_1.values(), range(10)):
            self.assertEqual(ii, str(jj))

    def test_items(self):
        for ii, jj in self.dict_view_1.items():
            self.assertEqual(str(ii), jj)
