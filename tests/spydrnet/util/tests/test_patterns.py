import unittest
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


class TestPatterns(unittest.TestCase):
    def test_is_pattern_absolute(self):
        self.assertFalse(_is_pattern_absolute("MY_TEST", False, False))
        self.assertFalse(_is_pattern_absolute("MY_TEST", True, True))
        self.assertTrue(_is_pattern_absolute("MY_TEST", True, False))
        self.assertFalse(_is_pattern_absolute("*", True, False))
        self.assertFalse(_is_pattern_absolute(".*", True, True))

    def test_value_matches_pattern(self):
        self.assertTrue(_value_matches_pattern(None, "*", is_case=True, is_re=False))
        self.assertTrue(_value_matches_pattern(None, "*", is_case=False, is_re=False))
        self.assertTrue(_value_matches_pattern(None, ".*", is_case=True, is_re=True))
        self.assertTrue(_value_matches_pattern(None, ".*", is_case=False, is_re=True))

    def test_value_matches_pattern_bad_regex_expr(self):
        self.assertFalse(_value_matches_pattern(None, "*", is_case=False, is_re=True))

