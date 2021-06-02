from spydrnet.plugins.namespace_manager.default_namespace import DefaultNamespace
from spydrnet.ir import Netlist, Library, Definition
import re
from spydrnet.plugins.namespace_manager.default_namespace import DefaultNamespace


class EdifNamespace(DefaultNamespace):

    @classmethod
    def is_name_of_element_valid(cls, element):
        """
        All names are valid in the default namespace. Always returns true.
        :param element:
        :return: True
        """
        if "EDIF.identifier" in element:
            identifier = element["EDIF.identifier"]
            return cls._check_EDIF_identifier(identifier)
        return True

    @classmethod
    def is_name_valid(cls, key, value):
        if key == "EDIF.identifier":
            return cls._check_EDIF_identifier(value)
        return True

    @classmethod
    def _check_EDIF_identifier(cls, identifier):
        identifier_length = len(identifier)
        starts_with_ampersand = identifier.startswith("&")
        if starts_with_ampersand:
            if identifier_length < 2 or identifier_length > 256:
                return False
            return bool(re.match(r"^&[0-9A-Za-z_]+$", identifier))
        else:
            if identifier_length < 1 or identifier_length > 255:
                return False
            if identifier[0].isalpha() is False:
                return False
            return bool(re.match(r"^[0-9A-Za-z_]+$", identifier))

    @classmethod
    def no_name_conflicts(cls, element):
        """
        Check to see if there are any name conflicts among the children
        :param element:
        :return:
        """
        namespace = set()
        edif_namespace = set()
        if isinstance(element, Netlist):
            for library in element.libraries:
                if ".NAME" in library:
                    name = library[".NAME"]
                    if name not in namespace:
                        namespace.add(name)
                    else:
                        return False
                if "EDIF.identifier" in library:
                    identifier = library["EDIF.identifier"].lower()
                    if identifier not in edif_namespace:
                        edif_namespace.add(identifier)
                    else:
                        return False
        elif isinstance(element, Library):
            for definition in element.definitions:
                if ".NAME" in definition:
                    name = definition[".NAME"]
                    if name not in namespace:
                        namespace.add(name)
                    else:
                        return False
                if "EDIF.identifier" in definition:
                    identifier = definition["EDIF.identifier"].lower()
                    if identifier not in edif_namespace:
                        edif_namespace.add(identifier)
                    else:
                        return False
        elif isinstance(element, Definition):
            for port in element.ports:
                if ".NAME" in port:
                    name = port[".NAME"]
                    if name not in namespace:
                        namespace.add(name)
                    else:
                        return False
                if "EDIF.identifier" in port:
                    identifier = port["EDIF.identifier"].lower()
                    if identifier not in edif_namespace:
                        edif_namespace.add(identifier)
                    else:
                        return False
            namespace.clear()
            for cable in element.cables:
                if ".NAME" in cable:
                    name = cable[".NAME"]
                    if name not in namespace:
                        namespace.add(name)
                    else:
                        return False
                if "EDIF.identifier" in cable:
                    identifier = cable["EDIF.identifier"].lower()
                    if identifier not in edif_namespace:
                        edif_namespace.add(identifier)
                    else:
                        return False
            namespace.clear()
            for instance in element.children:
                if ".NAME" in instance:
                    name = instance[".NAME"]
                    if name not in namespace:
                        namespace.add(name)
                    else:
                        return False
                if "EDIF.identifier" in instance:
                    identifier = instance["EDIF.identifier"].lower()
                    if identifier not in edif_namespace:
                        edif_namespace.add(identifier)
                    else:
                        return False
        return True

    def __init__(self):
        self.namespaces = dict()
        self.edif_namespaces = dict()

    def no_conflict(self, element, key, value):
        element_type = type(element)
        if key == ".NAME":
            if element_type in self.namespaces:
                namespace = self.namespaces[element_type]
                if value in namespace:
                    if namespace[value] != element:
                        return False
        elif key == "EDIF.identifier":
            if element_type in self.edif_namespaces:
                namespace = self.edif_namespaces[element_type]
                value_lower = value.lower()
                if value_lower in namespace:
                    if namespace[value_lower] != element:
                        return False
        return True

    def update(self, element, key, value):
        element_type = type(element)
        if key == ".NAME":
            if element_type not in self.namespaces:
                self.namespaces[element_type] = dict()
            namespace = self.namespaces[element_type]
            if ".NAME" in element:
                old_name = element[".NAME"]
                if old_name in namespace:
                    del namespace[old_name]
            namespace[value] = element
        elif key == "EDIF.identifier":
            if element_type not in self.edif_namespaces:
                self.edif_namespaces[element_type] = dict()
            namespace = self.edif_namespaces[element_type]
            if "EDIF.identifier" in element:
                old_name = element["EDIF.identifier"].lower()
                if old_name in namespace:
                    del namespace[old_name]
            namespace[value.lower()] = element

    def remove(self, element, key):
        element_type = type(element)
        if key == ".NAME":
            if element_type in self.namespaces:
                namespace = self.namespaces[element_type]
                if ".NAME" in element:
                    old_name = element[".NAME"]
                    if old_name in namespace:
                        del namespace[old_name]
        elif key == "EDIF.identifier":
            if element_type in self.edif_namespaces:
                namespace = self.edif_namespaces[element_type]
                if "EDIF.identifier" in element:
                    old_name = element["EDIF.identifier"]
                    if old_name in namespace:
                        del namespace[old_name.lower()]

    def lookup(self, element_type, key, value):
        if key == ".NAME":
            if element_type in self.namespaces:
                namespace = self.namespaces[element_type]
                return namespace.get(value, None)
        elif key == "EDIF.identifier":
            if element_type in self.edif_namespaces:
                namespace = self.edif_namespaces[element_type]
                return namespace.get(value.lower(), None)
