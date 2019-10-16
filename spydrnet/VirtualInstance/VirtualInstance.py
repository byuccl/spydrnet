class VirtualInstance:

    nextUUID = 1
    identifier = 'EDIF.identifier'

    def __init__(self, instance):
        self.physical_instance = instance
        self.parent = None
        self.UUID = VirtualInstance.nextUUID
        VirtualInstance.nextUUID += 1
        self.children = set()

    def add_parent(self, instance):
        self.parent = instance

    def add_child(self, instance):
        self.children.add(instance)

    def get_name(self):
        name = self.physical_instance[VirtualInstance.identifier]
        parent = self.parent
        while parent is not None:
            name = parent.physical_instance[VirtualInstance.identifier] + '/' + name
            parent = parent.parent
        return name
