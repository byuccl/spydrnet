import unittest

from spydrnet.ir.views.setview import SetView


class TestSetView(unittest.TestCase):
    def setUp(self) -> None:
        self.set_view = SetView(set(range(10)))

    def test_and(self):
        self.assertEqual(len(set(range(10, 20)) & self.set_view), 0)
        self.assertEqual(len(self.set_view & set(range(10, 20))), 0)

    def test_or(self):
        self.assertEqual(len(set(range(10, 20)) | self.set_view), 20)
        self.assertEqual(len(self.set_view | set(range(10, 20))), 20)

    def test_min(self):
        self.assertEqual(len(set(range(10, 20)) - self.set_view), 10)
        self.assertEqual(len(self.set_view - set(range(10, 20))), 10)

    def test_xor(self):
        self.assertEqual(len(set(range(10, 20)) ^ self.set_view), 20)
        self.assertEqual(len(self.set_view ^ set(range(10, 20))), 20)

    @unittest.expectedFailure
    def test_and_assignment(self):
        self.set_view &= set(range(5))

    @unittest.expectedFailure
    def test_or_assignment(self):
        self.set_view |= set(range(5))

    @unittest.expectedFailure
    def test_min_assignment(self):
        self.set_view -= set(range(5))

    @unittest.expectedFailure
    def test_xor_assignment(self):
        self.set_view ^= set(range(5))

    def test_hash(self):
        self.assertRaises(TypeError, hash, self.set_view)

    def test_eq(self):
        self.assertTrue(self.set_view == set(range(10)))
        self.assertTrue(self.set_view == SetView(set(range(10))))

    def test_ne(self):
        self.assertFalse(self.set_view != set(range(10)))
        self.assertFalse(self.set_view != SetView(set(range(10))))

    def test_ge(self):
        self.assertTrue(self.set_view >= set(range(10)))
        self.assertTrue(self.set_view >= SetView(set(range(10))))

    def test_le(self):
        self.assertTrue(self.set_view <= set(range(10)))
        self.assertTrue(self.set_view <= SetView(set(range(10))))

    def test_gt(self):
        self.assertFalse(self.set_view > set(range(10)))
        self.assertFalse(self.set_view > SetView(set(range(10))))

    def test_lt(self):
        self.assertFalse(self.set_view < set(range(10)))
        self.assertFalse(self.set_view < SetView(set(range(10))))

    def test_len(self):
        self.assertTrue(len(self.set_view), 10)

    def test_repr(self):
        self.assertEqual(repr(self.set_view), repr(set(range(10))))

    def test_str(self):
        self.assertEqual(str(self.set_view), str(set(range(10))))

    def test_copy(self):
        self.assertEqual(set(range(10)), self.set_view.copy())

    def test_difference(self):
        self.assertEqual(set(range(5)), self.set_view.difference(set(range(5, 10))))

    def test_intersection(self):
        self.assertEqual(set(range(5)), self.set_view.intersection(set(range(5))))

    def test_isdisjoint(self):
        self.assertTrue(self.set_view.isdisjoint(set(range(10, 20))))

    def test_issubset(self):
        self.assertTrue(self.set_view.issubset(set(range(20))))

    def test_issuperset(self):
        self.assertTrue(self.set_view.issuperset(set(range(5))))

    def test_symmetric_difference(self):
        self.assertTrue(set(range(10)) ^ set(range(5, 20)), self.set_view.symmetric_difference(set(range(5, 20))))

    def test_union(self):
        self.assertTrue(set(range(20)), self.set_view.union(set(range(10, 20))))

