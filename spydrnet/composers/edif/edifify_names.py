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
    >>> import spydrnet as sdn
    >>> ed = EdififyNames()
    >>> i = sdn.Instance()
    >>> i.name = "*this_is+an$*`id[0:3]"
    >>> l = [i]
    >>> valid_identifier = ed.make_valid(i,l)

    The valid_identifier should be the following:

    &_this_is_an___in_0_3_

    >>> import spydrnet as sdn
    >>> i = sdn.Instance()
    >>> i.name = 'name'
    >>> i2 = sdn.Instance()
    >>> i2.name = 'name_sdn_1_'
    >>> i3 = sdn.Instance()
    >>> i3.name = 'name'
    >>> my_list = [i,i2,i3]
    >>> ed.make_valid(i3, my_list)

    The output should be the following:

    name_sdn_2_

    """

    def __init__(self):
        self.valid = set()
        self.non_alpha = set()
        self.name_length_target = 100

    def _length_good(self, identifier):
        """returns a boolean indicating whether or not the indentifier fits the 256 character limit"""

        return len(identifier) < self.name_length_target

    def _length_fix(self, identifier):
        """returns the name with the fixed length of 256 characters if the limit is exceeded"""
        if not self._length_good(identifier):
            pattern = re.compile('_sdn_[0-9]+_$')
            r = pattern.search(identifier)
            if r is None:
                return identifier[:self.name_length_target]
            else:
                return identifier[:self.name_length_target - (r.end() - r.start())] + identifier[r.start():]
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
        identifier = self._length_fix(identifier)
        return identifier

    def _conflicts_good(self, obj, identifier, objects):
        for element in objects:
            if element == obj:
                continue
            if element.name == identifier or ("EDIF.identifier" in element.data and element["EDIF.identifier"] == identifier):
                return False
        return True

    def _conflicts_fix(self, obj, identifier, objects):
        identifier_lower = identifier.lower()
        if not self._conflicts_good(obj, identifier_lower, objects):
            pattern = re.compile('_sdn_[0-9]+_$')
            r = pattern.search(identifier_lower)
            if r is None:
                identifier_lower = identifier_lower + '_sdn_1_'
            else:
                # get the number out of the string
                num = int(
                    re.search(r'\d+', identifier_lower[r.start():]).group())
                identifier_lower = identifier_lower[:r.start(
                )+5] + str(num + 1) + '_'
            identifier_lower = self._length_fix(identifier_lower)
            identifier_lower = self._conflicts_fix(
                obj, identifier_lower, objects)
            identifier = identifier_lower
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

    def make_valid(self, obj, objects):
        """
        make a compliant identifier based on the identifier given.
        returns the identifier if no change is needed.
        """
        identifier = obj.name
        identifier = self._length_fix(identifier)
        identifier = self._characters_fix(identifier)
        identifier = self._conflicts_fix(obj, identifier, objects)

        return identifier
