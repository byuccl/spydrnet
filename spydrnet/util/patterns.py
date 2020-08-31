import fnmatch
import re


def _is_pattern_absolute(pattern, is_case, is_re):
    if is_case is False or is_re is True:
        return False
    else:
        for char in pattern:
            if char in {"*", "?"}:
                return False
    return True


def _value_matches_pattern(value, pattern, is_case, is_re):
    if value is None:
        value = ""
    if is_re:
        try:
            if re.fullmatch(pattern, value, flags=0 if is_case else re.IGNORECASE):
                return True
        except re.error:
            return False
    elif is_case:
        return fnmatch.fnmatchcase(value, pattern)
    else:
        return fnmatch.fnmatch(value, pattern)