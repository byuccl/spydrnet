
_global_flags = {
    'use_case_sensitive_naming' : True
}

def _get_global_flag(name):
    return _global_flags[name]

def _set_global_flag(name, value):
    global _global_flags
    _global_flags[name] = value

def use_case_sensitive_naming():
    return _get_global_flag('use_case_sensitive_naming')

def set_use_case_sensitive_naming(use_case_sensitive_naming):
    _set_global_flag('use_case_sensitive_naming', use_case_sensitive_naming)
