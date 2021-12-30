import unittest

from spydrnet.ir import FirstClassElement, Bundle


class TestFirstClassElement(unittest.TestCase):

    def setUp(self) -> None:
        ''' Test setup '''
        self.fElement = FirstClassElement()
        self.fElement.name = "dummy"

    def test_extended_method(self):
        ''' test extended_method '''
        self.assertEqual(self.fElement.first_class_extended(),
                         {'.NAME': 'dummy'})
