import unittest

from spydrnet.ir import Element, Bundle


class TestElement(unittest.TestCase):

    def setUp(self) -> None:
        ''' Test setup '''
        self.element = Element()

    def test_extended_method(self):
        ''' test extended_method '''
        self.assertEqual(self.element.extended_method(), 'Extended')
