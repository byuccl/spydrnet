#Copyright 2021
#Author Dallin Skouson
#see the license for details
#
#Tests the verilog composers functions and output

import unittest
import spydrnet as sdn
from spydrnet import composers

class TestVerilogComposerUnit(unittest.TestCase):
    
    class TestFile:
        '''represents a file (has a write function for the composer)
        can be used as a drop in replacement for the composer file.write function
        saves all written stuff to a string'''
        def __init__(self):
            self.written = ""

        def write(self, text):
            self.written += text
        
        def clear(self):
            self.written = ""
        