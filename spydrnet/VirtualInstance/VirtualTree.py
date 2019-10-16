from spydrnet.VirtualInstance.VirtualInstance import VirtualInstance

class VirtualTree:

    def __init__(self):
        self.root = None

    def build_tree(self, ir):
        self.root = VirtualInstance(ir.top_instance)
        self._add_children(self.root)

    def _add_children(self, virtual_instance):
        parent = virtual_instance.physical_instance
        for instance in parent.definition.instances:
            vi = VirtualInstance(instance)
            vi.add_parent(virtual_instance)
            self._add_children(vi)
            virtual_instance.add_child(vi)




from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
import spydrnet.support_files as files

def printNames(root):
    print(root.get_name())
    vi = list(root.children)
    while len(vi) != 0:
        temp = vi.pop()
        vi.extend(list(temp.children))
        print(temp.get_name())

if __name__ == '__main__':
    parser = EdifParser.from_filename(files.edif_files['TMR_hierarchy.edf'])
    parser.parse()
    ir = parser.netlist
    tree = VirtualTree()
    tree.build_tree(ir)
    root = tree.root
    printNames(root)