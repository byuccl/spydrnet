
'''
The callback manager is responsible for listening to changes in the ir and calling registered functions when those changes happen.

The changes that are listened for are the following:
object addition
object removal
object name change of objects

each change has the following functions:

Add.register
Add._do

Remove.register
Remove._do

NameChange.register
NameChange._do

there is also a register function at the top level that will register a function for all types of changes.

the register function will put a function pointer into a queue which is called when the corresponding function is called.

when registering a listener function the function must comply with the following format:

'''

class AddCallback:
    
    functions = []

    @classmethod
    def register(cls, function):
        cls.functions.append(function)

    @classmethod
    def _do(cls, element_to_add, parent_element):
        for f in cls.functions:
            f(element_to_add)


class RemoveCallback:
    
    functions = []

    @classmethod
    def register(cls, function):
        cls.functions.append(function)

    @classmethod
    def _do(cls, element_to_remove):
        for f in cls.functions:
            f(element_to_remove)

class RenameCallback:
    functions = []

    @classmethod
    def register(cls, function):
        cls.functions.append(function)

    @classmethod
    def _do(cls, element_to_rename, new_name):
        for f in cls.functions:
            f(element_to_rename, new_name)
