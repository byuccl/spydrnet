import unittest
import os
import glob

import spydrnet.tests as st
from spydrnet.parsers.edif.tokenizer import EdifTokenizer

class TestCompareNetlists(unittest.TestCase):
	
	def test_edif(self):		
		# glob all tests
		edif_files = glob.glob(os.path.join(st.testdata_dir,"*.edf.zip"))
		for filename in edif_files:
			print(filename)
			# 1 read edif
			# 2 compose
			# 3 read composed
			# 4 compare
			# assert compare good
		
		self.assertTrue(False, "We need to implement a test to recursively check all test edif.")
		
if __name__ == '__main__':
    unittest.main()