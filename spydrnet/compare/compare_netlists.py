from spydrnet.ir import OuterPin
import spydrnet as sdn


class Comparer:

    def __init__(self, ir_orig, ir_composer):
        assert ir_orig and ir_composer, "Both orig_netlist and composer netlist must be specified"
        self.ir_orig = ir_orig
        self.ir_composer = ir_composer

    def run(self):
        self.compare()

    def compare(self):
        # try:
        assert self.get_identifier(self.ir_orig) == self.get_identifier(self.ir_composer), \
            "Environments do not have the same identifier"
        assert self.get_original_identifier(self.ir_orig) == self.get_original_identifier(self.ir_composer), \
            "Environments do not have the same original identifier"
        # if there is no top instance in either then this test passes.
        if (self.ir_composer.top_instance != None or self.ir_orig.top_instance != None):
            self.compare_instances(
                self.ir_orig.top_instance, self.ir_composer.top_instance)
        assert len(self.ir_orig.libraries) == len(self.ir_composer.libraries), \
            "Environments do not have the same number of libraries"
        # except Exception:
        #     import pdb; pdb.set_trace()
        for orig_library in self.ir_orig.libraries:
            if orig_library.name == None:
                # ports with no name are not compared
                print("WARNING: library with name == None exists and is not compared")
                continue
            else:
                patterns = orig_library.name
            composer_library = next(
                sdn.get_libraries(self.ir_composer, patterns))
            self.compare_libraries(orig_library, composer_library)

    def compare_libraries(self, library_orig, library_composer):
        # try:
        assert self.get_identifier(library_orig) == self.get_identifier(library_composer), \
            "Libraries do not have the same identifier"
        assert self.get_original_identifier(library_orig) == self.get_original_identifier(library_composer), \
            "Libraries do not have the same original identifier"
        assert len(library_orig.definitions) == len(library_composer.definitions), \
            "Libraries do not have the same amount of definitions " \
            + str(library_orig) + " " + str(len(library_orig.definitions)) + " " +\
            str(library_composer) + " " + \
            str(len(library_composer.definitions))
        # except Exception:
        #     import pdb; pdb.set_trace()
        for orig_definition in library_orig.definitions:
            if orig_definition.name == None:
                # ports with no name are not compared
                print(
                    "WARNING: definitions with name == None exist but are not compared")
                continue
            else:
                patterns = orig_definition.name
            composer_definition = next(
                sdn.get_definitions(library_composer, patterns))
            self.compare_definition(orig_definition, composer_definition)

    def compare_definition(self, definition_orig, definition_composer, check_identifier=True):
        if check_identifier:
            assert self.get_identifier(definition_orig) == self.get_identifier(definition_composer), \
                "Definitions do not have the same identifier"
            assert self.get_original_identifier(definition_orig) == self.get_original_identifier(definition_composer), \
                "Definitions do not have the same original identifier"

        assert len(definition_orig.ports) == len(definition_composer.ports), \
            "Definitions do not have the same number of ports"
        # for orig_port, composer_port in zip(definition_orig.ports, definition_composer.ports):
        #     self.compare_ports(orig_port, composer_port)
        # do a smarter compare
        for orig_port in definition_orig.ports:
            if orig_port.name == None:
                # ports with no name are not compared
                print("WARNING: ports with name == None exist and are not compared")
                continue
            else:
                patterns = orig_port.name
            composer_port = next(sdn.get_ports(definition_composer, patterns))
            self.compare_ports(orig_port, composer_port)

        assert len(definition_orig.cables) == len(definition_composer.cables), \
            "Definitions do not have the same number of cables "\
            + definition_orig.name + " " + str(len(definition_orig.cables))\
            + " " + definition_composer.name + " " + \
            str(len(definition_composer.cables))

        for orig_cable in definition_orig.cables:
            if orig_cable.name == None:
                # ports with no name are not compared
                print("WARNING: cables with name == None exist and are not compared")
                continue
            else:
                patterns = orig_cable.name
            composer_cable = next(sdn.get_cables(
                definition_composer, patterns))
            self.compare_cables(orig_cable, composer_cable)

        assert len(definition_orig.children) == len(definition_composer.children), \
            "Definitions do not have the same number of instances"
        # for orig_instance, composer_cable in zip(definition_orig.children, definition_composer.children):
        #     self.compare_instances(orig_instance, composer_cable)
        for orig_instance in definition_orig.children:
            if orig_instance.name == None:
                # ports with no name are not compared
                print("WARNING: children with name == None exist and are not compared")
                continue
            else:
                if orig_instance.name.startswith("SDN_Assignment_"):
                    # skip assignment statements for now
                    continue
                else:
                    patterns = orig_instance.name

            composer_instance = next(
                sdn.get_instances(definition_composer, patterns))

            self.compare_instances(orig_instance, composer_instance)

        # compare assignemnt statements
        pattern = "SDN_Assignment_*"
        composer_generator = sdn.get_instances(definition_composer, pattern)
        orig_generator = sdn.get_instances(definition_orig, pattern)
        # i just need to make sure that they both contain the same number of each width assignment
        composer_dict = dict()
        orig_dict = dict()

        ci = next(composer_generator, None)
        while ci is not None:
            num = ci.name.split("_")[3]
            if num in composer_dict:
                composer_dict[num] += 1
            else:
                composer_dict[num] = 1
            ci = next(composer_generator, None)

        oi = next(orig_generator, None)
        while oi is not None:
            num = oi.name.split("_")[3]
            if num in orig_dict:
                orig_dict[num] += 1
            else:
                orig_dict[num] = 1
            oi = next(orig_generator, None)

        for k in composer_dict.keys():
            assert k in orig_dict and orig_dict[k] == composer_dict[k], "there are a different number of " + str(
                k) + " width assignment"

    def compare_cables(self, cable_orig, cable_composer):
        assert self.get_identifier(cable_orig) == self.get_identifier(cable_composer), \
            "Cables do not have the same identifier"
        assert self.get_original_identifier(cable_orig) == self.get_original_identifier(cable_composer), \
            "Cables do not have the same original identifier"
        assert len(cable_orig.wires) == len(cable_composer.wires), \
            "Cables do not have the same number of wires " + cable_orig.name + " " + \
            str(len(cable_orig.wires)) + " " + cable_composer.name + \
            " " + str(len(cable_composer.wires))
        # zip is left here because the order of wires in cables matters.
        for orig_wire, composer_wire in zip(cable_orig.wires, cable_composer.wires):
            assert len(orig_wire.pins) == len(composer_wire.pins), \
                "wires connect to a different number of pins " + \
                orig_wire.cable.name + " " + composer_wire.cable.name
            for orig_pin, composer_pin in zip(orig_wire.pins, composer_wire.pins):
                assert type(orig_pin) == type(composer_pin), \
                    "pin types do not match up."
                if isinstance(orig_pin, OuterPin):
                    self.compare_outer_pins(orig_pin, composer_pin)
                else:
                    self.compare_inner_pins(orig_pin, composer_pin)

    def compare_outer_pins(self, pin_orig, pin_composer):
        assert pin_orig.instance.reference == pin_orig.inner_pin.port.definition and \
            pin_composer.instance.reference == pin_composer.inner_pin.port.definition, \
            "DRC failure, outer pin instance reference on associated pin definition not the same"
        # try:
        assert self.are_instances_equivalent(pin_orig.instance, pin_composer.instance), \
            "Net does not connect to a pin on the same instance"
        # except Exception:
        #     import pdb; pdb.set_trace()

        assert self.are_inner_pins_equivalent(pin_orig.inner_pin, pin_orig.inner_pin), \
            "Net does not connect the same pin"

    def compare_inner_pins(self, pin_orig, pin_composer):
        assert self.are_inner_pins_equivalent(pin_orig, pin_composer), \
            "Net does not connect the same pin"

    def are_instances_equivalent(self, orig_instance, composer_instance):
        orig_name = self.get_identifier(orig_instance)
        composer_name = self.get_identifier(composer_instance)
        # assignment instances are not very well kept when written out so just compare the width
        if orig_name.startswith("SDN_Assignment_") and composer_name.startswith("SDN_Assignment_"):
            orig_split = orig_name.split("_")
            composer_split = composer_name.split("_")
            assert orig_split[3] == composer_split[3], "the widths of the assignments are off " + \
                orig_split[3] + " " + composer_split[3]
        else:
            assert orig_name == composer_name, "Names are not the same " + \
                orig_name + " " + composer_name
        assert self.get_identifier(orig_instance.reference) == self.get_identifier(composer_instance.reference) and \
            self.get_identifier(orig_instance.reference.library) == \
            self.get_identifier(composer_instance.reference.library) and \
            self.get_identifier(orig_instance.parent) == self.get_identifier(composer_instance.parent) and \
            self.get_identifier(orig_instance.parent.library) == \
            self.get_identifier(composer_instance.parent.library), \
            'Instances are not equivalent ' + orig_instance.name + " " + composer_instance.name
        return True

    def are_inner_pins_equivalent(self, orig_pin, composer_pin):
        assert orig_pin.port.pins.index(orig_pin) == composer_pin.port.pins.index(composer_pin), \
            "Pin indices do not match"
        assert self.get_identifier(orig_pin.port) == self.get_identifier(composer_pin.port) and \
            self.get_identifier(orig_pin.port.definition) == self.get_identifier(composer_pin.port.definition) and \
            self.get_identifier(orig_pin.port.definition.library) == \
            self.get_identifier(composer_pin.port.definition.library), \
            "Pins are not from equivalent ports"
        return True

    def compare_ports(self, port_orig, port_composer):
        assert self.get_identifier(port_orig) == self.get_identifier(port_composer), \
            "Ports do not have the same identifier"
        assert self.get_original_identifier(port_orig) == self.get_original_identifier(port_composer), \
            "Ports do not have the same original identifier"

        assert port_orig.direction == port_composer.direction, \
            "Ports are not facing the same direction, " + \
            str(port_orig.direction) + " " + str(port_composer.direction)

        assert port_orig.is_array == port_composer.is_array, \
            "Ports Array mismatch"

        assert len(port_orig.pins) > 0 and len(port_composer.pins) > 0, \
            "DRC failure, ports should have at least one pin"

        assert len(port_orig.pins) == len(port_composer.pins), \
            "Ports do not have the same number of pins, " + port_orig.name + " " + \
            str(len(port_orig.pins)) + " " + port_composer.name + \
            " " + str(len(port_composer.pins))

        assert self.get_identifier(port_orig.definition) == self.get_identifier(port_composer.definition) and \
            self.get_identifier(port_orig.definition.library) == \
            self.get_identifier(port_composer.definition.library), \
            "Ports do not belong to an equivalent definition"

    def compare_instances(self, instances_orig, instances_composer):
        instances_orig_identifier = self.get_identifier(instances_orig)
        instances_composer_identifier = self.get_identifier(instances_composer)
        assert instances_orig_identifier == instances_composer_identifier, \
            "Instances do not have the same identifier, orig \"{}\" " \
            "composer \"{}\"".format(
                instances_orig_identifier, instances_composer_identifier)

        instances_orig_original_identifier = self.get_original_identifier(
            instances_orig)
        instances_composer_original_identifier = self.get_original_identifier(
            instances_composer)
        assert instances_orig_original_identifier == instances_composer_original_identifier, \
            "Instances do not have the same original identifier, orig " \
            "\"{}\" composer \"{}\"".format(
                instances_orig_original_identifier, instances_composer_original_identifier)

        assert (instances_orig.reference == None and instances_composer.reference == None) or \
            (self.get_identifier(instances_orig.reference) == self.get_identifier(instances_composer.reference) and
             self.get_identifier(instances_orig.reference.library) ==
             self.get_identifier(instances_composer.reference.library)), \
            "Instances do not have the same reference definition."

        if "EDIF.properties" in instances_orig:
            assert "EDIF.properties" in instances_composer, "Composer is missing properties"
            properties_orig = instances_orig["EDIF.properties"]
            properties_composer = instances_composer["EDIF.properties"]
            for x in range(len(properties_orig)):
                for key, value in properties_orig[x].items():
                    assert properties_orig[x][key] == properties_composer[x][key], \
                        "Instances do not have the same properties"

    @staticmethod
    def get_identifier(obj):
        if obj == None:
            return None
        return obj.name
        # if "EDIF.identifier" in obj:
        #     return obj["EDIF.identifier"]

    @staticmethod
    def get_original_identifier(obj):
        if obj == None:
            return None
        if "EDIF.original_identifier" in obj:
            return obj["EDIF.original_identifier"]
