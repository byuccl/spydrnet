import unittest
import os

from spydrnet.transform.util import find_object, build_name
from spydrnet.transform.replicate import Replicator
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.ir import *

class TestReplicater(unittest.TestCase):

    def test_trace_pin(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        test = find_object(ir, 'y_OBUF_inst_i_1/O', 'port')
        replicate = Replicator(ir=ir)
        pin = replicate.find_other_side(test.inner_pins[0])
        ports = replicate.trace_pin(pin)
        self.assertTrue(len(ports) == 1)
        for port in ports:
            self.assertTrue(port.__getitem__('EDIF.identifier') == 'b')

    def test_replicate_port(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        port = find_object(ir, "delta/omega/b", 'port')
        num_of_ports = len(port.definition.ports)
        replicate = Replicator(ir=ir)
        new_port = replicate.replicate_port(port, 1)
        self.assertTrue(new_port.__getitem__('EDIF.identifier') == 'b_TMR_1')
        self.assertTrue(len(new_port.inner_pins) == len(port.inner_pins))
        self.assertTrue(new_port.direction == port.direction)
        self.assertTrue(new_port.definition == port.definition)
        self.assertTrue(new_port.parent == port.parent)
        self.assertTrue(len(port.definition.ports) == num_of_ports + 1)

    def test_replicate_ports(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        target = ['b_INST_0', 'beta_INST_0']
        replicate.replicate_ports(target)
        ports = replicate.ports
        self.assertTrue(len(ports) == 1)
        for key, value in ports.items():
            self.assertTrue(len(value) == 2)

    def test_trace_cable(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        cable = find_object(ir, 'delta/alpha_2_', 'cable')
        cables = replicate.trace_cable(cable)
        self.assertTrue(len(cables) == 2)

    def test_identify_cables(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        target = ['b_INST_0', 'beta_INST_0']
        cables = replicate._identify_cables_(target)
        self.assertTrue(len(cables) == 12)

    def test_copy_properties(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        original_instance = find_object(ir, "delta/omega/b_INST_0", "instance")
        instance = Instance()
        replicate._copy_properties_(instance, original_instance)
        for property in original_instance._metadata["EDIF.properties"]:
            self.assertTrue(property in instance._metadata["EDIF.properties"])

    def test_add_suffix_instance(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        instance = find_object(ir, "delta/omega/b_INST_0", "instance")
        old_identifier = instance.__getitem__("EDIF.identifier")
        replicate._add_suffix(instance, "_TMR")
        self.assertTrue(instance.__getitem__("EDIF.identifier") == old_identifier + "_TMR")

    def test_add_suffix_multi_bit_wire(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        cable = find_object(ir, "delta/alpha[1]", "cable")
        old_identifier = cable.__getitem__("EDIF.identifier")
        old_originial_identifer = cable.__getitem__("EDIF.original_identifier")
        replicate._add_suffix(cable, "_TMR")
        # cable = Cable()
        # cable.__setitem__("EDIF.identifier", "alpha_1_")
        # cable.__setitem__("EDIF.original_identifier", "alpha[1]")
        # replicate._add_suffix(cable, "_TMR")
        self.assertTrue(cable.__getitem__("EDIF.identifier") == old_identifier + "_TMR")
        self.assertTrue(cable.__getitem__("EDIF.original_identifier") == "alpha_TMR[1]")

    def test_copy_instance(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        instance = find_object(ir, "delta/beta_INST_0", "instance")
        new_instance = replicate._copy_instance_(instance)
        self.assertFalse(instance == new_instance)
        self.assertTrue(instance.definition == new_instance.definition)
        for inner_pin, outter_pin in instance.outer_pins.items():
            self.assertTrue(inner_pin in new_instance.outer_pins)
            self.assertFalse(outter_pin == new_instance.outer_pins[inner_pin])

    def test_port_position(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        port = find_object(ir, "delta/alpha", "port")
        for true_position in range(len(port.inner_pins)):
            guessed_position = replicate.port_position(port.inner_pins[true_position], port)
            self.assertTrue(guessed_position == true_position)

    def test_is_connected_to_replicate_pin(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        cable1 = find_object(ir, "delta/alpha[0]", "cable")
        cable2 = find_object(ir, "delta/beta", "cable")
        port1 = find_object(ir, "delta/alpha", "port")
        port2 = find_object(ir, "delta/omega/a", "port")
        replicate.ports = {port1: None}
        self.assertTrue(replicate.is_connected_to_replicate_pin(cable1))
        replicate.ports = {port2: None}
        self.assertTrue(replicate.is_connected_to_replicate_pin(cable1))
        self.assertFalse(replicate.is_connected_to_replicate_pin(cable2))

    def test_create_cable(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        cable = find_object(ir, "delta/alpha[0]", "cable")
        new_cable = replicate.create_cable(cable, 1)
        self.assertFalse(cable == new_cable)
        self.assertTrue(new_cable.__getitem__("EDIF.identifier") == "alpha_0__TMR_1")
        self.assertTrue(new_cable.__getitem__("EDIF.original_identifier") == "alpha_TMR_1[0]")

    def test_connect_cable_to_port(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        cable = find_object(ir, "delta/alpha[0]", "cable")
        port = find_object(ir, "delta/omega/a", "port")
        wire = Wire()
        new_port = replicate.replicate_port(port, 1)
        replicate.ports = {port: [new_port]}
        replicate.connect_cable_to_port(cable, 1, wire)
        self.assertTrue(wire.pins[0].inner_pin in new_port.inner_pins)
        self.assertTrue(wire.pins[0].inner_pin.port.__getitem__("EDIF.identifier") == "a_TMR_1")
        port = find_object(ir, "delta/alpha", "port")
        new_port = replicate.replicate_port(port, 1)
        replicate.ports = {port: [new_port]}
        wire = Wire()
        replicate.connect_cable_to_port(cable, 1, wire)
        self.assertTrue(wire.pins[0] in new_port.inner_pins)
        self.assertTrue(wire.pins[0].port.__getitem__("EDIF.identifier") == "alpha_TMR_1")

    def test_connect_cable_to_cells(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        cell = find_object(ir, "delta/omega/b_INST_0", "instance")
        new_cell = replicate._copy_instance_(cell)
        wire = Wire()
        group = {cell: new_cell}
        cable = find_object(ir, "delta/omega/a[0]", "cable")
        replicate.connect_cable_to_cells(cable, group, wire)
        self.assertTrue(wire.pins[0].inner_pin in new_cell.outer_pins)
        self.assertTrue(wire.pins[0] == new_cell.outer_pins[wire.pins[0].inner_pin])

    def test_connect_nets(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        target = ["b_INST_0"]
        cell = find_object(ir, "delta/omega/b_INST_0", "instance")
        new_cell = replicate._copy_instance_(cell)
        replicate._add_suffix(new_cell, "_TMR")
        cell.parent_definition.add_instance(new_cell)
        added_cells = [{cell: new_cell}]
        replicate._connect_nets_(target, added_cells)
        cable = find_object(ir, "delta/omega/b_TMR_1", "cable")
        self.assertTrue(cable.wires[0].pins[0].instance == new_cell)
        for inner_pin, outer_pin in new_cell.outer_pins.items():
            if inner_pin.port.direction == Port.Direction.OUT:
                self.assertTrue(outer_pin.wire.cable.__getitem__("EDIF.identifier") == "b_TMR_1")
            else:
                self.assertTrue(outer_pin.wire.cable.__getitem__("EDIF.identifier") == "a_0_"
                                or outer_pin.wire.cable.__getitem__("EDIF.identifier") == "a_1_")

    def test_replicate_cell(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        target = ["b_INST_0"]
        added_cells = replicate._replicate_cells_(target)
        self.assertTrue(len(added_cells) == 2)
        x = 1
        for group in added_cells:
            self.assertTrue(len(group) == 1)
            for cell, new_cell in group.items():
                self.assertTrue(cell.parent_definition == new_cell.parent_definition)
                self.assertTrue(cell.definition == new_cell.definition)
                for property in cell._metadata["EDIF.properties"]:
                    self.assertTrue(property in new_cell._metadata["EDIF.properties"])
                self.assertTrue(new_cell.__getitem__("EDIF.identifier") == target[0] + "_TMR_" + str(x))
            x += 1

    def test_all(self):
        parser = EdifParser.from_filename("TMR_hierarchy.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        targets = ['b_INST_0', 'beta_INST_0']
        replicate.run(targets)
        for x in range(1, 3):
            for target in targets:

                temp = replicate.cells[target]
                for key, temp in  temp.outer_pins.items():
                    break
                temp = temp.wire.cable
                build_name(ir, temp)

                cell = find_object(ir, target, "instance")
                new_cell = find_object(ir, target + "_TMR_" + str(x), "instance")
                self.assertTrue(cell.parent_definition == new_cell.parent_definition)
                self.assertTrue(cell.definition == new_cell.definition)
                for property in cell._metadata["EDIF.properties"]:
                    self.assertTrue(property in new_cell._metadata["EDIF.properties"])
                self.assertTrue(new_cell.__getitem__("EDIF.identifier") == target + "_TMR_" + str(x))
            port = find_object(ir, "delta/omega/b" + "_TMR_" + str(x), "port")
            self.assertFalse(port is None)
            cable = find_object(ir, "delta/omega/b" + "_TMR_" + str(x), "cable")
            for pin in cable.wires[0].pins:
                if isinstance(pin, OuterPin):
                    self.assertTrue(pin.instance.__getitem__("EDIF.identifier") == "b_INST_0_TMR_" + str(x))
                    self.assertTrue(pin.inner_pin.port.__getitem__("EDIF.identifier") == "O")
                else:
                    self.assertTrue(pin.port.__getitem__("EDIF.identifier") == "b_TMR_" + str(x))
            cable = find_object(ir, "delta/temp" + "_TMR_" + str(x), "cable")
            check1 = False
            check2 = False
            for pin in cable.wires[0].pins:
                if pin.inner_pin.port.__getitem__("EDIF.identifier") == "b_TMR_" + str(x):
                    check1 = True
                elif pin.inner_pin.port.__getitem__("EDIF.identifier") == "I0":
                    if pin.instance.__getitem__("EDIF.identifier") == "beta_INST_0_TMR_" + str(x):
                        check2 = True
            self.assertTrue(check1 and check2)
            cable = find_object(ir, "delta/beta" + "_TMR_" + str(x), "cable")
            self.assertTrue(len(cable.wires[0].pins) == 1)

    def test_cable_connecting_replicated_ports(self):
        parser = EdifParser.from_filename("ports_diff_modules.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        target = ["b_INST_0", "d_INST_0"]
        replicate.run(target)
        ports_set_one = set()
        ports_set_two = set()
        port = find_object(ir, "a/b_TMR_1", "port")
        self.assertFalse(port is None)
        ports_set_one.add(port)
        port = find_object(ir, "a/b_TMR_2", "port")
        self.assertFalse(port is None)
        ports_set_two.add(port)
        port = find_object(ir, "b/c_TMR_1", "port")
        self.assertFalse(port is None)
        ports_set_one.add(port)
        port = find_object(ir, "b/c_TMR_2", "port")
        self.assertFalse(port is None)
        ports_set_two.add(port)
        cable = find_object(ir, "temp_TMR_1", "cable")
        self.assertFalse(cable is None)
        for pin in cable.wires[0].pins:
            self.assertTrue(pin.inner_pin.port in ports_set_one)
        cable = find_object(ir, "temp_TMR_2", "cable")
        self.assertFalse(cable is None)
        for pin in cable.wires[0].pins:
            self.assertTrue(pin.inner_pin.port in ports_set_two)
        print()

    def test_port_replicate_one_instance(self):
        parser = EdifParser.from_filename("multi_port.edf")
        parser.parse()
        ir = parser.netlist
        replicate = Replicator(ir=ir)
        replicate._process_ir_()
        target = ["m_1__INST_0", "ut_OBUF_inst_i_1"]
        replicate.run(target)
        ports = set()
        ports.add(find_object(ir, "phoenix/m", "port"))
        ports.add(find_object(ir, "phoenix/m_TMR_1", "port"))
        ports.add(find_object(ir, "phoenix/m_TMR_2", "port"))
        cable = find_object(ir, "phoenix/m_1_", "cable")
        for pin in cable.wires[0].pins:
            if isinstance(pin, OuterPin):
                continue
            self.assertTrue(pin.port in ports)
        print()

import shutil
import glob
import zipfile
import csv

import spydrnet.tests as st
import spydrnet.tests as hello
from spydrnet.composers.edif.composer import ComposeEdif

class TestReplicaterRegression(unittest.TestCase):
    def setUp(self):
        replicator = Replicator()

    def test_run(self):
        # parser = EdifParser.from_filename("TMR_hierarchy.edf")
        # parser.parse()
        # ir = parser.netlist
        # target = ["b_INST_0", "beta_INST_0"]
        # replicator = Replicator()
        # replicator.run(target, ir)
        # replicated_instance = self.check_instance_replication(ir, target, replicator.cells)
        # ports = self.check_port_replication(ir, target, replicator.cells)
        # replicated_cables = self.check_cable_replication(ports[0], replicator.cells, ir, target)
        # self.check_cable_connection(replicated_instance, ports[1], replicated_cables)

        if os.path.exists("temp"):
            shutil.rmtree("temp")
        if os.path.exists("errors.txt"):
            os.remove("errors.txt")

        test = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        edif_files = sorted(glob.glob(os.path.join(test, "*.edf.zip")), key=os.path.getsize)
        passed = True

        for filename in edif_files:
            print(filename)
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall("temp")
            zip_ref.close()
            edif_file = glob.glob("temp/*.edf")
            target_file = glob.glob("temp/*.csv")

            parser = EdifParser.from_filename(edif_file[0])
            parser.parse()
            ir = parser.netlist

            with open(target_file[0]) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    target = row

            replicator = Replicator()
            replicator.run(target, ir)

            composer = ComposeEdif()
            composer.run(ir, "temp/out.edf")

            replicated_instance = self.check_instance_replication(ir, target, replicator.cells)
            ports = self.check_port_replication(ir, target, replicator.cells)
            replicated_cables = self.check_cable_replication(ports[0], replicator.cells, ir, target)
            self.check_cable_connection(replicated_instance, ports[1], replicated_cables)

            if os.path.exists("temp"):
                shutil.rmtree("temp", ignore_errors=True)
            print()

            print()


        # Unzip test file
        # Read in netlist
        # Read in targets
        # Run replicator
        # Check to see if the instances were replicated corrected
        # Check to see if the correct ports were replicated
        # Check to see if the correct cables were replicated
        # Check to see if the replicated cables are connected to correct instances/ports
        pass

    def check_instance_replication(self, ir, targets, cells):
        replicated_instance = list()
        for replicate in range(1, 3):
            for target in targets:
                _ = build_name(ir, cells[target])
                instance = find_object(ir, _ + "_TMR_" + str(replicate), "instance")
                self.assertFalse(instance is None)
                replicated_instance.append(instance)
        unreplicated_instances = set(cells).difference(set(targets))
        for replicate in range(1, 3):
            for instance in unreplicated_instances:
                _ = build_name(ir, cells[instance])
                test = find_object(ir, _ + "_TMR_" + str(replicate), "instance")
                self.assertTrue(test is None)
        return replicated_instance

    def check_port_replication(self, ir, targets, cells):
        temp = list()
        for target in targets:
            temp.append(cells[target])
        replicated_ports = self.determine_replicate_ports(temp, ir)
        temp23 = list()
        ports = self.get_ports(ir)
        for replicate in range(1, 3):
            for port in replicated_ports:
                _ = build_name(ir, port)
                test = find_object(ir, _ + "_TMR_" + str(replicate), "port")
                self.assertFalse(test is None)
                temp23.append(test)
                ports.pop(test.__getitem__("EDIF.identifier"))
        test = set(ports)
        test = test.difference(set(replicated_ports))
        for port in replicated_ports:
            ports.pop(port.__getitem__("EDIF.identifier"))
        unreplicated_ports = set(ports).difference(replicated_ports)
        for replicate in range(1, 3):
            for port in unreplicated_ports:
                _ = build_name(ir, ports[port])
                test = find_object(ir, _ + "_TMR_" + str(replicate), "port")
                self.assertTrue(test is None)
        return [replicated_ports, temp23]

    def check_cable_replication(self, ports, cells, ir, targets):
        cables = self.get_cables(ir)
        pins = list()
        for target in targets:
            for inner_pin, outer_pin in cells[target].outer_pins.items():
                pins.append(outer_pin)
        for port in ports:
            test = build_name(ir, port)
            test = test.split('/')
            temp = ""
            for x in range(len(test) - 1):
                temp = test[x]
            test = find_object(ir, temp, "instance")
            outpin = test.outer_pins[port.inner_pins[0]]
            for inner_pin in port.inner_pins:
                pins.append(inner_pin)
                pins.append(test.outer_pins[inner_pin])
        replicated_cables = set()
        for pin in pins:
            if isinstance(pin, OuterPin) and pin.inner_pin.port.direction == Port.Direction.OUT:
                replicated_cables.add(pin.wire.cable)
            if isinstance(pin, InnerPin) and pin.port.direction == Port.Direction.IN:
                replicated_cables.add(pin.wire.cable)
            for temp in pin.wire.pins:
                if temp not in pins:
                    continue
                if temp == pin and not (isinstance(temp, OuterPin) and temp.inner_pin.port.direction == Port.Direction.OUT):
                    continue
                elif isinstance(temp, OuterPin) and temp.inner_pin.port.direction == Port.Direction.OUT:
                    replicated_cables.add(temp.wire.cable)
                elif isinstance(pin, OuterPin):
                    if isinstance(temp, OuterPin):
                        pass
        replicated_cables_ = dict()
        for replicate in range(1, 3):
            for cable in replicated_cables:
                _ = build_name(ir, cable)
                test = find_object(ir, _ + "_TMR_" + str(replicate), "cable")
                self.assertFalse(test is None)
                cables.pop(test.__getitem__("EDIF.identifier"))
                try:
                    cables.pop(cable.__getitem__('EDIF.identifier'))
                except KeyError:
                    pass
                replicated_cables_[test.__getitem__("EDIF.identifier")] = test
        for replicate in range(1, 3):
            for key, cable in cables.items():
                _ = build_name(ir, cable)
                test = find_object(ir, _ + "_TMR_" + str(replicate), "cable")
                self.assertTrue(test is None)
        return replicated_cables_

    def check_cable_connection(self, replicated_cells, replicated_ports, replicated_cables):
        for replicated_cell in replicated_cells:
            replicate = replicated_cell.__getitem__("EDIF.identifier")[-6:]
            for key, pin in replicated_cell.outer_pins.items():
                cable = pin.wire.cable
                name = cable.__getitem__("EDIF.identifier")
                length = len(name)
                if length > 6 and name[-6:-1] == "_TMR_":
                    self.assertTrue(name[-6:] == replicate)
                else:
                    self.assertFalse(name + replicate in replicated_cables)
        pass
        for replicated_port in replicated_ports:
            replicate = replicated_port.__getitem__("EDIF.identifier")[-6:]
            for pin in replicated_port.inner_pins:
                cable = pin.wire.cable
                name = cable.__getitem__("EDIF.identifier")
                length = len(name)
                if length > 6 and name[-6:-1] == "_TMR_":
                    self.assertTrue(name[-6:] == replicate)
                else:
                    self.assertFalse(name + replicate in replicated_cables)
        for key, replicated_cable in replicated_cables.items():
            replicate = replicated_cable.__getitem__("EDIF.identifier")[-6:]
            for pin in replicated_cable.wires[0].pins:
                if isinstance(pin, OuterPin):
                    temp = pin.instance.__getitem__("EDIF.identifier")[-6:]
                    test = pin.instance.__getitem__("EDIF.identifier")[-6:] == replicate
                    port = pin.inner_pin.port
                    self.assertTrue(pin.instance.__getitem__("EDIF.identifier")[-6:] == replicate
                                    or port.__getitem__("EDIF.identifier")[-6:] == replicate)
                else:
                    self.assertTrue(pin.port.__getitem__("EDIF.identifier")[-6:] == replicate)

    def determine_replicate_ports(self, cells, ir):
        output_pin = set()
        input_pin = set()
        for cell in cells:
            for inner_pin, outer_pin in cell.outer_pins.items():
                if inner_pin.port.direction == Port.Direction.IN:
                    input_pin = input_pin.union(self.trace_pin(outer_pin, ir))
                else:
                    output_pin = output_pin.union(self.trace_pin(outer_pin, ir))
        ports = output_pin.intersection(input_pin)
        return ports

    def get_ports(self, ir):
        ports = dict()
        for library in ir.libraries:
            for definition in library.definitions:
                for port in definition.ports:
                    if port.__getitem__("EDIF.identifier") in ports:
                        if type(ports[port.__getitem__("EDIF.identifier")]) == Port:
                            ports[port.__getitem__("EDIF.identifier")] = [ports[port.__getitem__("EDIF.identifier")]]
                        ports[port.__getitem__("EDIF.identifier")].append(port)
                    ports[port.__getitem__("EDIF.identifier")] = port
        return ports

    def get_cables(self, ir):
        cables = dict()
        for library in ir.libraries:
            for definition in library.definitions:
                for cable in definition.cables:
                    if cable.__getitem__("EDIF.identifier") in cables:
                        if type(cables[cable.__getitem__("EDIF.identifier")]) == Port:
                            cables[cable.__getitem__("EDIF.identifier")] = [cables[cable.__getitem__("EDIF.identifier")]]
                        cables[cable.__getitem__("EDIF.identifier")].append(cable)
                    cables[cable.__getitem__("EDIF.identifier")] = cable
        return cables

    def trace_pin(self, pin, ir):
        ports = set()
        trash = set()
        stack = list()
        stack.append(pin)
        trash.add(pin)
        while len(stack) > 0:
            pin = stack.pop()
            for pin_ in pin.wire.pins:
                if pin_ not in trash:
                    stack.append(pin_)
                    if isinstance(pin_, InnerPin):
                        ports.add(pin_.port)
                        test = build_name(ir, pin_.port)
                        test = test.split('/')
                        temp =""
                        for x in range(len(test) - 1):
                            temp = test[x]
                        test = find_object(ir, temp, "instance")
                        if test is None:
                            continue
                        for key, value in test.outer_pins.items():
                            if key == pin_:
                                if value not in trash:
                                    trash.add(value)
                                    stack.append(value)
                    else:
                        if pin_.inner_pin.wire is not None:
                            ports.add(pin_.inner_pin.port)
                            if pin_.inner_pin not in trash:
                                stack.append(pin_.inner_pin)
                                trash.add(pin_.inner_pin)
                    trash.add(pin_)
        return ports


if __name__ == '__main__':
    unittest.main()
