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