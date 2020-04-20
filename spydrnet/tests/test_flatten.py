
import unittest
import spydrnet as sdn
from spydrnet.ir import *
from spydrnet.flatten import flatten
from spydrnet.uniquify import uniquify

class TestUniquify(unittest.TestCase):
    def create_netlist(self):
        nl = Netlist()
        lib = nl.create_library()
        d1 = lib.create_definition()
        d1.name = ("d1")
        d2 = lib.create_definition()
        d2.name = ("d2")
        d3 = lib.create_definition()
        d3.name = ("d3")
        i11 = d1.create_child()
        i11.name = ("i11")
        i12 = d1.create_child()
        i12.name = ("i12")
        i13 = d1.create_child()
        i13.name = ("i13")
        i24 = d2.create_child()
        i24.name = ("i24")
        i25 = d2.create_child()
        i25.name = ("i25")
        i26 = d2.create_child()
        i26.name = ("i26")
        i27 = d2.create_child()
        d4 = lib.create_definition()
        d4.name = ("d4")
        i27.name = ("i27")
        i38 = d3.create_child()
        i38.name = ("i38")
        i39 = d3.create_child()
        i39.name = ("i39")
        i11.reference = d3
        i12.reference = d3
        i13.reference = d3
        i24.reference = d1
        i25.reference = d1
        i26.reference = d3
        i27.reference = d3
        i38.reference = d4
        i39.reference = d4
        nl.top_instance = Instance()
        nl.top_instance.reference = d2
        nl.top_instance.name = ("top_instance")
        return nl

    def create_mem_bus(self,top, proc, mem):
        mem_width = 10
        mem_write_out = proc.create_port()
        mem_write_out.name = "mem_write_out"
        mem_write_out.create_pins(mem_width)
        mem_read_in = proc.create_port()
        mem_read_in.name = "mem_read_in"
        mem_read_in.create_pins(mem_width)

        mem_write_in = mem.create_port()
        mem_write_in.name = "mem_write_in"
        mem_write_in.create_pins(mem_width)
        mem_read_out = mem.create_port()
        mem_read_out.name = "mem_read_out"
        mem_read_out.create_pins(mem_width)

        mem_write = top.create_cable()
        mem_write.name = "mem_write"
        mem_write.create_wires(mem_width)

        mem_read = top.create_cable()
        mem_read.name = "mem_read"
        mem_read.create_wires(mem_width)

        proc_i = top.create_child()
        proc_i.name = "proc_i"
        proc_i.reference = proc
        mem_i = top.create_child()
        mem_i.name = "mem_i"
        mem_i.reference = mem

        for i in range(mem_width):
            mem_write.wires[i].connect_pin(mem_i.pins[mem_write_in.pins[i]])
            mem_write.wires[i].connect_pin(proc_i.pins[mem_write_out.pins[i]])
            mem_read.wires[i].connect_pin(mem_i.pins[mem_read_out.pins[i]])
            mem_read.wires[i].connect_pin(proc_i.pins[mem_read_in.pins[i]])

        return mem_write_out, mem_read_in


    def create_proc(self, proc, mem_write, mem_read, core, cachel2):
        mem_width = 10
        core_i1 = proc.create_child()
        core_i2 = proc.create_child()
        core_i1.reference = core
        core_i2.reference = core
        core_i1.name = "core_i1"
        core_i2.name = "core_i2"

        mem_p = core.create_port()
        mem_p.create_pins(mem_width)
        mem_p.name = "mem_p"

        cachel2_i = proc.create_child()
        cachel2_i.reference = cachel2
        cachel2_i.name = "cachel2_i"
        
        mem_a_in  = cachel2.create_port()
        mem_a_out = cachel2.create_port()
        mem_b_in  = cachel2.create_port()
        mem_b_out = cachel2.create_port()
        
        
        mem_a_in.create_pins(mem_width)
        mem_a_out.create_pins(mem_width)
        mem_b_in.create_pins(mem_width)
        mem_b_out.create_pins(mem_width)

        mem_a_in.name = "mem_a_in"
        mem_b_out.name = "mem_a_out"
        mem_b_out.name = "mem_b_out"
        mem_b_in.name = "mem_b_in"
        
        
        ca1 = proc.create_cable()
        ca2 = proc.create_cable()
        cb1 = proc.create_cable()
        cb2 = proc.create_cable()

        ca1.create_wires(mem_width)
        ca2.create_wires(mem_width)
        cb1.create_wires(mem_width)
        cb2.create_wires(mem_width)

        ca1.name = "ca1"
        ca2.name = "ca2"
        cb1.name = "cb1"
        cb2.name = "cb2"

        for i in range(mem_width):
           ca1.wires[i].connect_pin(core_i1.pins[mem_p.pins[i]])
           ca1.wires[i].connect_pin(cachel2_i.pins[mem_a_in.pins[i]])
           ca2.wires[i].connect_pin(mem_read.pins[i])
           ca2.wires[i].connect_pin(cachel2_i.pins[mem_a_out.pins[i]])
           cb1.wires[i].connect_pin(core_i2.pins[mem_p.pins[i]])
           cb1.wires[i].connect_pin(cachel2_i.pins[mem_b_in.pins[i]])
           cb2.wires[i].connect_pin(mem_write.pins[i])
           cb2.wires[i].connect_pin(cachel2_i.pins[mem_b_out.pins[i]])

        return mem_p

    def create_core(self, core, mem_p, alu, reg_file):
        mem_width = 10
        alu_i = core.create_child()
        reg_file_i = core.create_child()
        
        alu_i.reference = alu
        alu_i.name = "alu_i"
        reg_file_i.reference = reg_file
        reg_file_i.name = "reg_file_i"

        alu_p = alu.create_port()
        reg_p = reg_file.create_port()

        alu_p.create_pins(mem_width)
        reg_p.create_pins(mem_width)
        alu_p.name = "alu_p"
        reg_p.name = "reg_p"

        mem_cable = core.create_cable()

        mem_cable.create_wires(mem_width)
        mem_cable.name = "mem_cable"

        for i in range(mem_width):
            mem_cable.wires[i].connect_pin(reg_file_i.pins[reg_p.pins[i]])
            mem_cable.wires[i].connect_pin(alu_i.pins[alu_p.pins[i]])
            mem_cable.wires[i].connect_pin(mem_p.pins[i])

    def create_netlist_with_wires(self):
        nl = Netlist()
        lib = nl.create_library()
        top = lib.create_definition()
        top.name = "top"
        proc = lib.create_definition()
        proc.name = "proc"
        core = lib.create_definition()
        core.name = "core"
        alu = lib.create_definition()
        alu.name = "alu"
        mem = lib.create_definition()
        mem.name = "mem"
        cachel2 = lib.create_definition()
        cachel2.name = "cacheL2"
        reg_file = lib.create_definition()
        reg_file.name = "reg_file"
        nl.top_instance = Instance()
        nl.top_instance.reference = top

        
        mem_write, mem_read= self.create_mem_bus(top, proc, mem)

        core_mem = self.create_proc(proc, mem_write, mem_read, core, cachel2)

        self.create_core(core, core_mem, alu, reg_file)

        nl.top_instance.name = ("top_instance")
        
        #self.simple_recursive_netlist_visualizer(nl)

        return nl



    # def simple_recursive_netlist_visualizer(self, netlist):
    #     #TODO put this code somewhere where people can use it to visualize simple netlists
    #     top_instance = netlist.top_instance
    #     #should look something like this:
    #     #top
    #     #   child1
    #     #       child1.child
    #     #   child2
    #     #       child2.child
    #     def recurse(instance, depth):
    #         s = depth * "\t"
    #         print(s, instance.name, "(", instance.reference.name, ")")
    #         for c in instance.reference.children:  
    #             recurse(c, depth + 1)
        
    #     recurse(top_instance, 0)

    def simple_cable_connection_visualizer(self,netlist):
        top_instance = netlist.top_instance
        #display all the cables in the top instance with all of their connections next to it
        def recur(instance):
            print(instance.name)
            for c in instance.reference.cables:
                print("\t(cable): ", c.name)
                if len(c.wires) > 0:
                    w = c.wires[0]
                    for p in w.pins:
                        if isinstance(p,OuterPin):
                            print("\t\t(instance): ", p.instance.name)
                        else:
                            print("\t\t(port):     ", p.port.name)
            for i in instance.reference.children:
                recur(i)

        recur(top_instance)


    def is_flat(self,nl):
        ti = nl.top_instance
        td = ti.reference
        for i in td.children:
            if not i.reference.is_leaf():
                return False
        return True



    def test_flatten_instances(self):
        nl = self.create_netlist()
        uniquify(nl)
        flatten(nl)
        assert self.is_flat(nl)


    def test_flatten_cables(self):
        nl = self.create_netlist_with_wires()
        self.simple_cable_connection_visualizer(nl)
        
        uniquify(nl)
        flatten(nl)
        self.simple_cable_connection_visualizer(nl)
        
        assert self.is_flat(nl) #might be nice to add some tests for the connections here.