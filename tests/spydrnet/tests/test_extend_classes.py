import unittest

'''try importing it and extending the classes. Then make sure they're actually extended'''

class TestExtendingClasses(unittest.TestCase):
    def test_import_and_extend(self):
        from spydrnet.ir import FirstClassElement
        from spydrnet.ir import Element
        # spydrnet_extension should have been imported and used to extend classes
        class1 = FirstClassElement()
        self.assertTrue("first_class_extended" in dir(class1))
        class2 = Element()
        self.assertTrue("extended_method" in dir(class2))
