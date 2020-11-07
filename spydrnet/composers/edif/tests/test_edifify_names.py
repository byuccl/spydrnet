import unittest
import spydrnet as sdn
from spydrnet.composers.edif.edifify_names import EdififyNames


class TestEdififyNames(unittest.TestCase):

    def test_simple_conversion(self):
        ed = EdififyNames()
        l = list()
        l = []
        assert ed.make_valid("name", l) == "name"

    def test_invalid_name(self):
        ed = EdififyNames()
        l = list()
        l = []
        assert ed.make_valid(
            "*this_is+an$*`id[0:3]", l) == "&_this_is_an___id_0_3_"

    def test_duplicate_name(self):
        ed = EdififyNames()
        l = list()
        i = sdn.Instance()
        i.name = 'name'
        l = [i]
        assert ed.make_valid("name", l) == "name_sdn_1_"

    def test_duplicate_number_increment(self):
        ed = EdififyNames()
        l = list()
        i = sdn.Instance()
        i.name = 'name'
        i2 = sdn.Instance()
        i2.name = 'name_sdn_1_'
        l = [i, i2]
        assert ed.make_valid("name", l) == "name_sdn_2_"

    def test_length(self):
        ed = EdififyNames()
        l = list()
        l = []
        test_str = ""
        answer_str = ""
        for i in range(105):
            test_str = test_str + 'a'
        for i in range(100):
            answer_str = answer_str + 'a'
        assert ed.make_valid(test_str, l) == answer_str

    def test_length_2(self):
        ed = EdififyNames()
        l = list()
        l = []
        test_str = "$"
        answer_str = "&_"
        for i in range(105):
            test_str = test_str + 'a'
        for i in range(98):
            answer_str = answer_str + 'a'
        assert ed.make_valid(test_str, l) == answer_str

    def test_length_3(self):
        ed = EdififyNames()
        l = list()

        instance_1 = sdn.Instance()
        name_1 = '&_'
        for i in range(98):
            name_1 = name_1 + 'a'
        instance_1.name = name_1

        instance_2 = sdn.Instance()

        name_2 = '&_'
        for i in range(91):
            name_2 = name_2 + 'a'
        name_2 = name_2 + '_sdn_1_'
        instance_2.name = name_2

        l = [instance_1, instance_2]
        test_str = '$'
        answer_str = '&_'
        for i in range(105):
            test_str = test_str + 'a'
        for i in range(91):
            answer_str = answer_str + 'a'

        answer_str = answer_str + '_sdn_2_'
        assert ed.make_valid(test_str, l) == answer_str
