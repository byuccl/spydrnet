import unittest
import spydrnet as sdn
from spydrnet.composers.edif.edifify_names import EdififyNames


class TestEdififyNames(unittest.TestCase):

    def test_simple_conversion(self):
        ed = EdififyNames()
        l = list()
        i = sdn.Instance()
        i.name = "name"
        l = [i]
        assert ed.make_valid(i, l) == "name"

    def test_invalid_name(self):
        ed = EdififyNames()
        l = list()
        i = sdn.Instance()
        i.name = "*this_is+an$*`id[0:3]"
        l = [i]
        assert ed.make_valid(
            i, l) == "&_this_is_an___id_0_3_"

    def test_duplicate_name(self):
        ed = EdififyNames()
        l = list()
        i = sdn.Instance()
        i.name = 'name'
        i2 = sdn.Instance()
        i2.name = 'name'
        l = [i, i2]
        assert ed.make_valid(i2, l) == "name_sdn_1_"

    def test_duplicate_number_increment(self):
        ed = EdififyNames()
        l = list()
        i = sdn.Instance()
        i.name = 'name'
        i_duplicate = sdn.Instance()
        i_duplicate.name = 'name'
        i2 = sdn.Instance()
        i2.name = 'name_sdn_1_'
        l = [i, i2, i_duplicate]
        assert ed.make_valid(i_duplicate, l) == "name_sdn_2_"

    def test_length(self):
        ed = EdififyNames()
        l = list()
        test_str = ""
        answer_str = ""
        for _ in range(ed.name_length_target + 5):
            test_str = test_str + 'a'
        for _ in range(ed.name_length_target):
            answer_str = answer_str + 'a'
        i = sdn.Instance()
        i.name = test_str
        l = [i]
        assert ed.make_valid(i, l) == answer_str

    def test_length_2(self):
        ed = EdififyNames()
        l = list()
        test_str = "$"
        answer_str = "&_"
        for _ in range(ed.name_length_target + 5):
            test_str = test_str + 'a'
        for _ in range(ed.name_length_target - 2):
            answer_str = answer_str + 'a'
        i = sdn.Instance()
        i.name = test_str
        l = [i]
        assert ed.make_valid(i, l) == answer_str

    def test_length_3(self):
        ed = EdififyNames()
        l = list()

        instance_1 = sdn.Instance()
        name_1 = '&_'
        for _ in range(ed.name_length_target - 2):
            name_1 = name_1 + 'a'
        instance_1.name = name_1

        instance_2 = sdn.Instance()

        name_2 = '&_'
        for _ in range(ed.name_length_target - 9):
            name_2 = name_2 + 'a'
        name_2 = name_2 + '_sdn_1_'
        instance_2.name = name_2

        test_str = '$'
        answer_str = '&_'
        for _ in range(ed.name_length_target + 5):
            test_str = test_str + 'a'
        for _ in range(ed.name_length_target - 9):
            answer_str = answer_str + 'a'

        answer_str = answer_str + '_sdn_2_'

        instance_3 = sdn.Instance()
        instance_3.name = test_str

        l = [instance_1, instance_2, instance_3]

        assert ed.make_valid(instance_3, l) == answer_str
