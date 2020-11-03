import re


class EdififyNames:
    """
    Handles the renaming of objects from other languages to EDIF. Emphasis
    is currently given to verilog.

    The following are differences between the namespaces of EDIF and Verilog.

    EDIF identifiers:

     * less than 256 characters in length (255 max)
     * a-z,A-Z,_,0-9 are valid characters
     * if non alphabetic character is first character prefix with &
     * case insensitive

    Verilog identifiers:

     * 1024 characters or less in length (1024 max)
     * a-z,A-Z,_,0-9 are valid characters. first character not digit (when unescpaed)
     * case sensitive
     * identifier starting with backslash is escaped
     * escaped identifiers can contain any ascii character except white space

    This class applys an approach similar to vivado to create the rename

     * shorten identifiers of too great a length then postfix with a unique id
     * replace invalid characters with _
     * conflicts when case insensitivity is used are postfixed with a unique id
     * names that end up matching other names are postfixed with a unique id

    Examples
    --------
    >>> from spydrnet.composers.edif.edifify_names import EdififyNames
    >>> ed = EdififyNames()
    >>> l = list()
    >>> ed.make_valid("*this_is+an$*`id[0:3]",l)

    The output should be the following:

    &_this_is_an___in_0_3_

    >>> import spydrnet as sdn
    >>> i = sdn.Instance()
    >>> i.name = 'hello'
    >>> i2 = sdn.Instance()
    >>> i2.name = 'hello_sdn_1_'
    >>> l = [i,i2]
    >>> ed.make_valid("hello",l)

from spydrnet.composers.edif.edifify_names import EdififyNames
ed = EdififyNames()
l = list()
import spydrnet as sdn
i = sdn.Instance()
i.name = 'hello'
i2 = sdn.Instance()
i2.name = 'hello_sdn_1_'
l = [i,i2]
ed.make_valid("hello",l)

    ABC...300
    abc...300


    \this_is+an$*`id[0:3]
    \this_is+an$^`id[3:4]

    &_this_is_an___in_0_3_
    name1
    name1_sdn_1_
    name1_sdn_2_

    """

    def __init__(self):
        self.valid = set()
        self.non_alpha = set()
        # valid.add("a")
        # valid.add("b")

    def _length_good(self, identifier):
        """returns a boolean indicating whether or not the indentifier fits the 256 character limit"""
        return len(identifier) < 256

    def _length_fix(self, identifier):
        """returns the name with the fixed length of 256 characters if the limit is exceeded"""
        if not self._length_good(identifier):
            regexp = re.compile('_sdn_[0-9]+_$')
            if regexp is None:
                return identifier[:100]
            else:
                return identifier[:100 - (regexp.end() + 1 - regexp.start())] + identifier[regexp.start():]
        else:
            return identifier

    def _characters_good(self, identifier):
        """Check if the characters meet the edif standards

        returns whether the string only contain numbers, characters and '-'
        """
        if not identifier[0].isalpha():
            return False
        for i in range(0, len(identifier)):
            if not identifier[i].isalnum() and identifier[i] != '-':
                return False
        return True

    def _characters_fix(self, identifier):
        """fix the characters so that it meets edif standards

        Add a '&' if the first character is not alphabetic
        replaces all the characters to '-' if it is not valid characters
        """
        if not self._characters_good(identifier):
            starting_index = 0
            if not identifier[0].isalpha():
                identifier = '&' + identifier[:]
                starting_index = 1

            for i in range(starting_index, len(identifier)):
                if not identifier[i].isalnum():
                    identifier = identifier[: i] + '_' + identifier[i+1:]
        return identifier

    def _conflicts_good(self, identifier, objects):
        for element in objects:
            if element.name == identifier:
                return False
        return True

    def _conflicts_fix(self, identifier, objects):

        if not self._conflicts_good(identifier, objects):
            pattern = re.compile('_sdn_[0-9]+_$')
            r = pattern.search(identifier)
            if r is None:
                identifier = identifier + '_sdn_1_'
            else:
                # get the number out of the string
                #num = [int(i) for i in identifier[0:].split() if i.isdigit()]
                num = int(re.search(r'\d+', identifier[r.start():]).group())
                identifier = identifier[:r.start()+5] + str(num + 1) + '_'
            identifier = self._conflicts_fix(identifier, objects)
        return identifier

    def is_valid_identifier(self, identifier):
        """
        check if the identifier is valid in the namespace that is set. Will also
        check to make sure the identifer is valid.
        """
        if self._length_good(identifier) is False:
            return False

        if self._characters_good(identifier) is False:
            return False
        return True

    def make_valid(self, identifier, objects):
        """
        make a compliant identifier based on the identifier given.
        returns the identifier if no change is needed.
        """

        identifier = self._length_fix(identifier)
        identifier = self._characters_fix(identifier)
        identifier = self._length_fix(identifier)
        identifier = self._conflicts_fix(identifier, objects)
        identifier = self._length_fix(identifier)

        return identifier
