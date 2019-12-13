import unittest
import os
import glob
import zipfile
import shutil
import logging
import traceback

from spydrnet.compare.compose_netlist import Composer
from spydrnet.compare.compare_netlists import Comparer
from spydrnet import base_dir

import pytest


class TestCompareNetlists(unittest.TestCase):
    @unittest.skip("Takes a long time")
    def test_edif(self):
        # glob all tests
        if os.path.exists("temp"):
            shutil.rmtree("temp")
        if os.path.exists("errors.txt"):
            os.remove("errors.txt")

        dir_of_edif_netlists = os.path.join(base_dir, "support_files", "EDIF_netlists")
        edif_files = sorted(glob.glob(os.path.join(dir_of_edif_netlists, "*.edf.zip")), key=os.path.getsize)
        passed = True
        for ii, filename in enumerate(edif_files):
            with self.subTest(i=ii):
                print(filename)
                zip_ref = zipfile.ZipFile(filename, 'r')
                zip_ref.extractall("temp")
                zip_ref.close()
                file = glob.glob("temp/*")
                print()
                # 1 read edif
                # 2 compose
                #try:
                composer = Composer(file[0], "temp/my_composed.edf")
                composer.run()
                composer = None
            # 3 read composed
            # 4 compare
                comparer = Comparer(file[0], "temp/my_composed.edf")
                comparer.run()
                comparer = None
                #except Exception as e:
                #    logging.error(str(type(e)) + str(e))
                #    my_file = open("errors3.txt", "a")
                #    my_file.write(filename)
                #    my_file.write('\n')
                #    my_file.write(str(type(e)))
                #    my_file.write(str(e))
                #    my_file.write('\n')
                #    test = traceback.format_exc().splitlines()
                #    for string in test:
                #        my_file.write(string)
                #        my_file.write('\n')
                #    my_file.write('\n')
                #    my_file.close()
                #    passed = False
                # assert compare good
                if os.path.exists("temp"):
                    shutil.rmtree("temp", ignore_errors=True)
            #print()
        self.assertTrue(passed)
        # self.assertTrue(False, "We need to implement a test to recursively check all test edif.")


if __name__ == '__main__':
    unittest.main()