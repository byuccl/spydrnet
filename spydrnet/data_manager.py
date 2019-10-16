import spydrnet.ir

class DataManager:
    @staticmethod
    def from_element_type_and_metadata_key(element_type, metadata_key):
        data_manager = DataManager(element_type, metadata_key)
        return data_manager

    def __init__(self, element_type, metadata_key):
        self.element_type = element_type
        self.metadata_key = metadata_key
        self.owner = None
        self._lookup = dict()

    def set_owner_and_populate_lookup(self, owner):
        self.owner = owner
        search_pool = [owner.children]
        while search_pool:
            children = search_pool.pop()
            for child in children:
                search_pool.append(child.children)
                self.add_to_lookup(child)

    def add_to_lookup(self, child):
        if type(child) == self.element_type:
            if self.metadata_key in child:
                metadata_value = child[self.metadata_key]
                metadata_value = self.condition_key(metadata_value)
                if metadata_value in self._lookup:
                    raise KeyError()
                else:
                    self._lookup[metadata_value] = child

    def lookup(self, cls, key, identifier):
        if cls == self.element_type and key == self.metadata_key:
            return self._lookup.get(self.condition_key(identifier))
        return None

    def get_all_children(self):
        return self._lookup.values()

    @staticmethod
    def condition_key(metadata_value):
        return metadata_value.lower()