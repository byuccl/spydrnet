import unittest

from spydrnet.ir.views.listview import ListView


class TestListView(unittest.TestCase):
    def setUp(self) -> None:
        self.list_view = ListView(list(range(10)))

    def test_getitem(self):
        self.assertTrue(self.list_view[0] == 0)

    def test_contains(self):
        self.assertTrue(5 in self.list_view)

    def test_comparison(self):
        list_copy = list(range(10))
        self.assertEqual(self.list_view, list_copy)
        empty_list = list()
        self.assertNotEqual(self.list_view, empty_list)

    def test_iter(self):
        aggregate = 0
        for item in self.list_view:
            aggregate += item
        self.assertEqual(sum(range(10)), aggregate)

    def test_len(self):
        self.assertEqual(len(self.list_view), 10)

    def test_reversed(self):
        self.assertEqual(next(iter(reversed(self.list_view))), 9)

    def test_copy(self):
        self.assertEqual(self.list_view, self.list_view.copy())

    def test_count(self):
        self.assertEqual(self.list_view.count(5), 1)

    def test_index(self):
        self.assertEqual(self.list_view.index(5), 5)

    def test_slice(self):
        self.assertEqual(self.list_view[1:4], list(range(1, 4)))

    def test_multiply(self):
        self.assertEqual(len(self.list_view * 2), 20)
        self.assertEqual(len(2 * self.list_view), 20)

    def test_add(self):
        result = list(range(10, 20)) + self.list_view
        print(result)
        self.assertEqual(len(result), 20)
        result = self.list_view + list(range(10, 20))
        print(result)
        self.assertEqual(len(result), 20)

    @unittest.expectedFailure
    def test_multiply_assignment(self):
        self.list_view *= 2

    @unittest.expectedFailure
    def test_add_assignment(self):
        self.list_view += list(range(10))

    def test_ge(self):
        self.assertTrue(self.list_view >= ListView(list(range(10))))
        self.assertTrue(self.list_view >= list(range(10)))

    def test_gt(self):
        self.assertTrue(self.list_view > ListView(list(range(9))))
        self.assertTrue(self.list_view > list(range(9)))

    def test_le(self):
        self.assertTrue(self.list_view <= ListView(list(range(10))))
        self.assertTrue(self.list_view <= list(range(10)))

    def test_lt(self):
        self.assertTrue(self.list_view < ListView(list(range(11))))
        self.assertTrue(self.list_view < list(range(11)))

    def test_repr(self):
        self.assertEqual(repr(self.list_view), repr(list(range(10))))

    def test_str(self):
        self.assertEqual(str(self.list_view), str(list(range(10))))

    def test_hash(self):
        self.assertRaises(TypeError, hash, self.list_view)
