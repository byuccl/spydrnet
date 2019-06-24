from spydrnet.parsers.edif.tokenizer import EdifTokenizer
from spydrnet.ir import *
from spydrnet.data_manager import DataManager
from spydrnet.parsers.edif.edif_tokens import *

from functools import reduce
import re


class EdifParser:
    def parse_construct(self, construct_parser):
        self.expect_begin_construct()
        result = construct_parser()
        self.expect_end_construct()
        return result

    @staticmethod
    def from_filename(filename):
        parser = EdifParser()
        parser.filename = filename
        return parser

    def __init__(self):
        self.filename = None
        self.elements = list()

    def parse(self):
        self.initialize_tokenizer()
        self.netlist = self.parse_construct(self.parse_edif)
        self.tokenizer.__del__()
        print("WARNING: edif/parser.py assumes downto in function parse_port()")

    def initialize_tokenizer(self):
        self.tokenizer = EdifTokenizer.from_filename(self.filename)

    def initialize_design(self):
        self.design = Design()
        self.design.netlist = Environment()

    def parse_edif(self):
        environment = Environment()
        environment.add_data_manager(DataManager.from_element_type_and_metadata_key(Library, 'EDIF.identifier'))
        self.append_new_element(environment)
        self.expect(EDIF)
        self.parse_nameDef()
        self.parse_header()
        self.parse_body()
        return self.pop_element()

    def parse_header(self):
        self.parse_construct(self.parse_edifVersion)
        self.parse_construct(self.parse_edifLevel)
        self.parse_construct(self.parse_keywordMap)

    def parse_edifVersion(self):
        self.expect(EDIF_VERSION)
        self.prefix_append('edifVersion')
        version_0 = self.parse_integerToken()
        version_1 = self.parse_integerToken()
        version_2 = self.parse_integerToken()
        self.set_attribute((version_0, version_1, version_2))
        self.prefix_pop()

    def parse_edifLevel(self):
        self.expect(EDIF_LEVEL)
        self.prefix_append('edifLevel')
        level = self.parse_integerToken()
        if level != 0:
            self.set_attribute(level)
        self.prefix_pop()

    def parse_keywordMap(self):
        self.expect(KEYWORD_MAP)
        self.prefix_append('keywordMap')
        self.parse_construct(self.parse_keywordLevel)

        while self.begin_construct():
            self.parse_construct(self.parse_comment)
        self.prefix_pop()

    def parse_keywordLevel(self):
        self.expect(KEYWORD_LEVEL)
        self.prefix_append('keywordLevel')
        level = self.parse_integerToken()
        if level != 0:
            self.set_attribute(level)
        self.prefix_pop()

    def parse_body(self):
        has_status = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()

            elif self.construct_is(EXTERNAL) or self.construct_is(LIBRARY):
                library = self.parse_library()
                environment = self.elements[-1]
                environment.add_library(library)

            elif self.construct_is(DESIGN):
                self.parse_design()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect("|".join([STATUS, EXTERNAL, LIBRARY, DESIGN, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_status(self):
        self.expect(STATUS)
        self.prefix_append('status')
        while self.begin_construct():
            if self.construct_is(WRITTEN):
                self.parse_written()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect("|".join([WRITTEN | COMMENT | USER_DATA]))
            self.expect_end_construct()
        self.prefix_pop()

    def parse_written(self):
        self.expect(WRITTEN)
        self.prefix_append('written')
        self.parse_construct(self.parse_timeStamp)

        has_author = False
        has_program = False
        has_dataOrigin = False
        while self.begin_construct():
            if self.construct_is(AUTHOR):
                has_author = self.check_for_multiples(AUTHOR, has_author)
                self.parse_author()

            elif self.construct_is(PROGRAM):
                has_program = self.check_for_multiples(PROGRAM, has_program)
                self.parse_program()

            elif self.construct_is(DATA_ORIGIN):
                has_dataOrigin = self.check_for_multiples(DATA_ORIGIN, has_dataOrigin)
                self.parse_dataOrigin()

            elif self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect("|".join([AUTHOR, PROGRAM, DATA_ORIGIN, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()
        self.prefix_pop()

    def parse_timeStamp(self):
        self.expect(TIME_STAMP)
        self.prefix_append('timeStamp')
        year = self.parse_integerToken()
        month = self.parse_integerToken()
        day = self.parse_integerToken()
        hour = self.parse_integerToken()
        minute = self.parse_integerToken()
        second = self.parse_integerToken()
        self.set_attribute((year, month, day, hour, minute, second))
        self.prefix_pop()

    def parse_author(self):
        self.expect(AUTHOR)
        self.prefix_append('author')
        author = self.parse_stringToken()
        self.set_attribute(author)
        self.prefix_pop()

    def parse_program(self):
        self.expect(PROGRAM)
        self.prefix_append('program')
        program = self.parse_stringToken()
        self.set_attribute(program)

        if self.begin_construct():
            self.expect(VERSION)
            self.prefix_append('version')
            version = self.parse_stringToken()
            self.set_attribute(version)
            self.prefix_pop()
            self.expect_end_construct()
        self.prefix_pop()

    def parse_library(self):
        library = Library()
        library.add_data_manager(DataManager.from_element_type_and_metadata_key(Definition, 'EDIF.identifier'))
        self.append_new_element(library)

        self.expect(LIBRARY)
        self.parse_nameDef()
        self.parse_construct(self.parse_edifLevel)
        self.parse_construct(self.parse_technology)

        has_status = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()

            elif self.construct_is(CELL):
                definition = self.parse_cell()
                library = self.elements[-1]
                library.add_definition(definition)
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect("|".join([STATUS, CELL, COMMENT, USER_DATA]))
            self.expect_end_construct()

        return self.pop_element()

    def parse_technology(self):
        self.expect(TECHNOLOGY)
        self.parse_construct(self.parse_numberDefinition)

    def parse_numberDefinition(self):
        self.expect(NUMBER_DEFINITION)
        while self.begin_construct():
            raise NotImplementedError()
            self.expect_end_construct()

    def parse_cell(self):
        definition = Definition()
        definition.add_data_manager(DataManager.from_element_type_and_metadata_key(Port, 'EDIF.identifier'))
        definition.add_data_manager(DataManager.from_element_type_and_metadata_key(Cable, 'EDIF.identifier'))
        definition.add_data_manager(DataManager.from_element_type_and_metadata_key(Instance, 'EDIF.identifier'))
        self.append_new_element(definition)

        self.expect(CELL)
        self.parse_nameDef()
        self.parse_construct(self.parse_cellType)

        has_status = False
        has_viewMap = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()

            elif self.construct_is(VIEW):
                self.parse_view()
            elif self.construct_is(VIEW_MAP):
                has_viewMap = self.check_for_multiples(VIEW_MAP, has_viewMap)
                self.parse_viewMap()

            elif self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([STATUS, VIEW, VIEW_MAP, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

        return self.pop_element()

    def parse_cellType(self):
        self.expect(CELL_TYPE)
        self.prefix_append("cellType")
        if self.construct_is(GENERIC) \
                or self.construct_is(TIE) \
                or self.construct_is(RIPPER):
            if not self.tokenizer.token_equals(GENERIC):
                self.set_attribute(self.tokenizer.token)
        else:
            self.expect("|".join([GENERIC, TIE, RIPPER]))
        self.tokenizer.next()
        self.prefix_pop()

    def parse_view(self):
        self.expect(VIEW)
        self.prefix_append('view')
        self.parse_nameDef()
        self.parse_construct(self.parse_viewType)
        self.parse_construct(self.parse_interface)

        has_status = False
        has_contents = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()

            elif self.construct_is(CONTENTS):
                has_contents = self.check_for_multiples(STATUS, has_contents)
                self.parse_contents()

            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([STATUS, CONTENTS, COMMENT, PROPERTY, USER_DATA]))
            self.expect_end_construct()
        self.prefix_pop()

    def parse_viewType(self):
        self.prefix_append('viewType')
        self.expect(VIEW_TYPE)
        if self.construct_is(BEHAVIOR) \
                or self.construct_is(DOCUMENT) \
                or self.construct_is(GRAPHIC) \
                or self.construct_is(LOGICMODEL) \
                or self.construct_is(MASKLAYOUT) \
                or self.construct_is(NETLIST) \
                or self.construct_is(PCBLAYOUT) \
                or self.construct_is(SCHEMATIC) \
                or self.construct_is(STRANGER) \
                or self.construct_is(SYMBOLIC):
            if not self.tokenizer.token_equals(NETLIST):
                self.set_attribute(self.tokenizer.token)
        else:
            self.expect("|".join(
                [BEHAVIOR, DOCUMENT, GRAPHIC, LOGICMODEL, MASKLAYOUT, NETLIST, PCBLAYOUT, SCHEMATIC, STRANGER,
                 SYMBOLIC]))
        self.tokenizer.next()
        self.prefix_pop()

    def parse_interface(self):
        self.expect(INTERFACE)
        while self.begin_construct():
            if self.construct_is(PORT):
                port = self.parse_port()
                cell = self.elements[-1]
                cell.add_port(port)

            elif self.construct_is(PORT_BUNDLE):
                raise NotImplementedError()
            elif self.construct_is(SYMBOL):
                raise NotImplementedError()
            elif self.construct_is(PROTECTION_FRAME):
                raise NotImplementedError()
            elif self.construct_is(ARRAY_RELATED_INFO):
                raise NotImplementedError()
            elif self.construct_is(PARAMETER):
                raise NotImplementedError()
            elif self.construct_is(JOINED):
                raise NotImplementedError()
            elif self.construct_is(MUST_JOIN):
                raise NotImplementedError()
            elif self.construct_is(WEAK_JOINED):
                raise NotImplementedError()
            elif self.construct_is(PERMUTABLE):
                raise NotImplementedError()
            elif self.construct_is(TIMING):
                raise NotImplementedError()
            elif self.construct_is(SIMULATE):
                raise NotImplementedError()
            elif self.construct_is(DESIGNATOR):
                raise NotImplementedError()
            elif self.construct_is(WEAK_JOINED):
                raise NotImplementedError()

            elif self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([PORT, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_port(self):
        self.append_new_element(Port())
        self.expect(PORT)
        if self.begin_construct():
            if self.construct_is(RENAME):
                self.parse_rename()
                port = self.elements[-1]
                port.initialize_pins(1)

            elif self.construct_is(ARRAY):
                dimension_sizes = self.parse_array()
                pin_count = reduce((lambda x, y: x * y), dimension_sizes)
                port = self.elements[-1]
                port.initialize_pins(pin_count)
                port.is_array = True
                if 'EDIF.original_identifier' in port:
                    # TODO: what about multi-dimensional ports, non-downto ports, and when non-square brackets are used <0:17><31:0>
                    original_identifier = port['EDIF.original_identifier']
                    match = re.match(r".*\[(\d+):(\d+)\]", original_identifier)
                    if match:
                        left_index = int(match.group(1))
                        right_index = int(match.group(2))
                        port.lower_index = min(right_index, left_index)

            else:
                self.expect('|'.join([RENAME, ARRAY]))
            self.expect_end_construct()
        else:
            self.parse_nameDef()
            port = self.elements[-1]
            port.initialize_pins(1)
            # TODO: what about single pin array ports with a non_zero starting index.

        has_direction = False
        while self.begin_construct():
            if self.construct_is(DIRECTION):
                has_direction = self.check_for_multiples(DIRECTION, has_direction)
                direction = self.parse_direction()
                port = self.elements[-1]
                port.direction = direction

            elif self.construct_is(UNUSED):
                raise NotImplementedError()
            elif self.construct_is(DESIGNATOR):
                raise NotImplementedError()
            elif self.construct_is(DC_FANIN_LOAD):
                raise NotImplementedError()
            elif self.construct_is(DC_FANOUT_LOAD):
                raise NotImplementedError()
            elif self.construct_is(DC_MAX_FANIN):
                raise NotImplementedError()
            elif self.construct_is(DC_MAX_FANOUT):
                raise NotImplementedError()
            elif self.construct_is(AC_LOAD):
                raise NotImplementedError()
            elif self.construct_is(PORT_DELAY):
                raise NotImplementedError()

            elif self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([DIRECTION, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()
        return self.elements.pop()

    def parse_array(self):
        self.expect(ARRAY)
        self.parse_nameDef()
        dimension_sizes = [self.parse_integerToken()]
        while self.tokenizer.is_valid_identifier():
            dimension_sizes.append(self.parse_integerToken())
        return dimension_sizes

    def parse_direction(self):
        self.expect(DIRECTION)
        direction = Port.Direction.UNDEFINED
        if self.construct_is(INOUT):
            direction = Port.Direction.INOUT
        elif self.construct_is(INPUT):
            direction = Port.Direction.IN
        elif self.construct_is(OUTPUT):
            direction = Port.Direction.OUT
        else:
            self.expect('|'.join([INOUT, INPUT, OUTPUT]))
        self.tokenizer.next()
        return direction

    def parse_contents(self):
        self.expect(CONTENTS)
        while self.begin_construct():
            if self.construct_is(INSTANCE):
                instance = self.parse_instance()
                definition = self.elements[-1]
                definition.add_instance(instance)

            elif self.construct_is(NET):
                cable = self.parse_net()
                definition = self.elements[-1]
                definition.add_cable(cable)

            elif self.construct_is(OFF_PAGE_CONNECTOR):
                raise NotImplementedError()
            elif self.construct_is(FIGURE):
                raise NotImplementedError()
            elif self.construct_is(SECTION):
                raise NotImplementedError()
            elif self.construct_is(NET_BUNDLE):
                raise NotImplementedError()
            elif self.construct_is(PAGE):
                raise NotImplementedError()
            elif self.construct_is(COMMENT_GRAPHICS):
                raise NotImplementedError()
            elif self.construct_is(PORT_IMPLEMENTATION):
                raise NotImplementedError()
            elif self.construct_is(TIMING):
                raise NotImplementedError()
            elif self.construct_is(SIMULATE):
                raise NotImplementedError()
            elif self.construct_is(WHEN):
                raise NotImplementedError()
            elif self.construct_is(FOLLOW):
                raise NotImplementedError()
            elif self.construct_is(LOGIC_PORT):
                raise NotImplementedError()
            elif self.construct_is(BOUNDING_BOX):
                raise NotImplementedError()
            elif self.construct_is(TIMING):
                raise NotImplementedError()

            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([INSTANCE, NET, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_instance(self):
        self.append_new_element(Instance())
        self.expect(INSTANCE)
        self.parse_nameDef()
        if self.begin_construct():
            if self.construct_is(VIEW_REF):
                definition = self.parse_viewRef()
                instance = self.elements[-1]
                instance.definition = definition

            elif self.construct_is(VIEW_LIST):
                raise NotImplementedError()
            else:
                self.expect(VIEW_REF)
            self.expect_end_construct()

        while self.begin_construct():
            if self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()
        return self.pop_element()

    def parse_viewRef(self):
        self.prefix_append('viewRef')
        self.expect(VIEW_REF)
        self.parse_nameRef()
        view_identifier = self.elements[-1].pop('EDIF.viewRef.identifier')
        definition = self.elements[-2]
        if self.begin_construct():
            definition = self.parse_cellRef()
            self.expect_end_construct()
        if definition['EDIF.view.identifier'].lower() != view_identifier.lower():
            raise RuntimeError("Parser error, non-existant view referenced on line {}, revieved {} expected {}".format(
                self.tokenizer.line_number, view_identifier, definition['EDIF.view.identifier']
            ))
        self.prefix_pop()
        return definition

    def parse_cellRef(self):
        self.prefix_append('cellRef')
        self.expect(CELL_REF)
        self.parse_nameRef()
        definition_identifer = self.elements[-1].pop('EDIF.viewRef.cellRef.identifier')
        library = self.elements[-3]
        if self.begin_construct():
            library = self.parse_libraryRef()
            self.expect_end_construct()
        definition = library.get_definition(definition_identifer)
        self.prefix_pop()
        return definition

    def parse_libraryRef(self):
        self.prefix_append('libraryRef')
        self.expect(LIBRARY_REF)
        self.parse_nameRef()
        library_identifier = self.elements[-1].pop('EDIF.viewRef.cellRef.libraryRef.identifier')
        environment = self.elements[-4]
        library = self.elements[-3]
        if library['EDIF.identifier'].lower() != library_identifier.lower():
            library = environment.get_library(library_identifier)
        self.prefix_pop()
        return library

    def parse_net(self):
        self.append_new_element(Cable())
        self.expect(NET)
        self.parse_nameDef()
        self.elements[-1].initialize_wires(1)  # EDIF nets are single wire cables.
        self.parse_construct(self.parse_joined)

        while self.begin_construct():
            if self.construct_is(PROPERTY):
                self.parse_property()
            elif self.construct_is(COMMENT):
                self.parse_comment()
            elif self.construct_is(USER_DATA):
                self.parse_userData()
            else:
                self.expect('|'.join([PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()
        return self.pop_element()

    def parse_joined(self):
        self.expect(JOINED)
        while self.begin_construct():
            if self.construct_is(PORT_REF):
                pin = self.parse_portRef()
                wire = self.elements[-1].get_wire(0)
                wire.connect_pin(pin)
            elif self.construct_is(PORT_LIST):
                raise NotImplementedError()
            elif self.construct_is(GLOBAL_PORT_REF):
                raise NotImplementedError()
            else:
                self.expect(PORT_REF)
            self.expect_end_construct()

    def parse_portRef(self):
        self.prefix_append('portRef')
        self.expect(PORT_REF)
        index = 0
        instance_or_definition = self.elements[-2]
        if self.begin_construct():
            indicies = self.parse_member()
            assert (len(indicies) == 1)
            index = indicies[0]
            self.expect_end_construct()
        else:
            self.parse_nameRef()

        while self.begin_construct():
            if self.construct_is(PORT_REF):
                raise NotImplementedError()
            elif self.construct_is(INSTANCE_REF):
                instance_or_definition = self.parse_instanceRef()
            elif self.construct_is(VIEW_REF):
                raise NotImplementedError()
            self.expect_end_construct()
        port_identifier = self.elements[-1].pop('EDIF.portRef.identifier')
        pin = instance_or_definition.get_pin(port_identifier, index)
        self.prefix_pop()
        return pin

    def parse_instanceRef(self):
        self.prefix_append('instanceRef')
        definition = self.elements[-2]
        self.expect(INSTANCE_REF)
        if self.begin_construct():
            self.parse_member()
            raise NotImplementedError()
            self.expect_end_construct()
        else:
            self.parse_nameRef()
        instance_identifier = self.elements[-1].pop('EDIF.portRef.instanceRef.identifier')
        instance = definition.get_instance(instance_identifier)
        self.prefix_pop()
        return instance

    def parse_member(self):
        self.expect(MEMBER)
        self.parse_nameDef()
        indicies = [self.parse_integerToken()]
        while self.not_end_construct():
            indicies.append(self.parse_integerToken())
            self.expect_end_construct()
        return indicies

    def parse_viewMap(self):
        self.expect(VIEW_MAP)
        raise NotImplementedError()

    def parse_design(self):
        self.expect(DESIGN)
        self.skip_until_next_construct()

    def parse_dataOrigin(self):
        self.expect(DATA_ORIGIN)
        raise NotImplementedError()

    def parse_userData(self):
        self.expect(USER_DATA)
        raise NotImplementedError()

    def parse_comment(self):
        self.prefix_append('comments')
        self.expect(COMMENT)
        comment = list()
        while self.not_end_construct():
            comment.append(self.parse_stringToken())
        comment = (*comment,)
        self.append_attribute(comment)
        self.prefix_pop()

    def parse_property(self):
        self.prefix_append('properties')
        self.expect(PROPERTY)
        self.parse_nameDef()

        property_ = dict()
        identifier = self.elements[-1].pop('.'.join([*self.elements[-1]['metadata_prefix'], 'identifier']))
        property_['identifier'] = identifier

        original_identifier_prefix = '.'.join([*self.elements[-1]['metadata_prefix'], 'original_identifier'])
        if original_identifier_prefix in self.elements[-1]:
            original_identifier = self.elements[-1].pop(original_identifier_prefix)
            property_['original_identifier'] = original_identifier

        value = self.parse_construct(self.parse_typedValue)
        property_['value'] = value

        self.append_attribute(property_)

        has_owner = False
        has_unit = False
        while self.begin_construct():
            if self.construct_is(OWNER):
                has_owner = self.check_for_multiples(OWNER, has_owner)
                raise NotImplementedError()  # self.parse_owner()

            elif self.construct_is(UNIT):
                has_unit = self.check_for_multiples(UNIT, has_unit)
                raise NotImplementedError()  # self.parse_unit()

            elif self.construct_is(PROPERTY):
                raise NotImplementedError()  # self.parse_property()
            elif self.construct_is(COMMENT):
                raise NotImplementedError()  # self.parse_comment()
            self.expect_end_construct()
        self.prefix_pop()

    def parse_typedValue(self):
        if self.construct_is(BOOLEAN):
            return self.parse_boolean()
        elif self.construct_is(INTEGER):
            return self.parse_integer()
        elif self.construct_is(MI_NO_MAX):
            raise NotImplementedError()
        elif self.construct_is(NUMBER):
            return self.parse_number()
        elif self.construct_is(POINT):
            raise NotImplementedError()
        elif self.construct_is(STRING):
            return self.parse_string()
        else:
            return self.expect('|'.join([BOOLEAN, INTEGER, NUMBER, STRING]))

    def parse_boolean(self):
        self.expect(BOOLEAN)
        self.expect_begin_construct()
        self.tokenizer.next()
        if self.tokenizer.token_equals(TRUE):
            result = True
        elif self.tokenizer.token_equals(FALSE):
            result = False
        else:
            self.expect('|'.join([TRUE, FALSE]))
        self.expect_end_construct()
        return result

    def parse_integer(self):
        self.expect(INTEGER)
        return self.parse_integerToken()

    def parse_number(self):
        self.expect(NUMBER)
        if self.begin_construct():
            result = self.parse_construct(self.parse_e)
            self.expect_end_construct()
        else:
            result = self.parse_integerToken()
        return result

    def parse_e(self):
        self.expect(E)
        mantissa = self.parse_integerToken()
        exponent = self.parse_integerToken()
        result = mantissa * 10.0 ** exponent
        return result

    def parse_string(self):
        self.expect(STRING)
        return self.parse_stringToken()

    def parse_owner(self):
        raise NotImplementedError()

    def parse_unit(self):
        raise NotImplementedError()

    def parse_nameRef(self):
        self.prefix_append('identifier')
        self.set_attribute(self.parse_identifier())
        self.prefix_pop()

    def parse_nameDef(self):
        if self.begin_construct():
            self.parse_rename()
            self.expect_end_construct()
        else:
            self.prefix_append('identifier')
            self.set_attribute(self.parse_identifier())
            self.prefix_pop()

    def parse_rename(self):
        self.expect(RENAME)

        self.prefix_append('identifier')
        self.set_attribute(self.parse_identifier())
        self.prefix_pop()

        self.prefix_append('original_identifier')
        self.set_attribute(self.parse_stringToken())
        self.prefix_pop()

    def parse_identifier(self):
        self.tokenizer.next()
        self.tokenizer.expect_valid_identifier()
        return self.tokenizer.token

    def parse_stringToken(self):
        self.tokenizer.next()
        self.tokenizer.expect_valid_stringToken()
        return self.tokenizer.token[1:-1]

    def parse_integerToken(self):
        self.tokenizer.next()
        self.tokenizer.expect_valid_integerToken()
        return int(self.tokenizer.token)

    def append_new_element(self, element):
        element['metadata_prefix'] = ['EDIF']
        self.elements.append(element)

    def pop_element(self):
        element = self.elements.pop()
        del element['metadata_prefix']
        return element

    def prefix_append(self, value):
        element = self.elements[-1]
        element['metadata_prefix'].append(value)

    def prefix_pop(self):
        return self.elements[-1]['metadata_prefix'].pop()

    def set_attribute(self, value):
        element = self.elements[-1]
        element['.'.join(element['metadata_prefix'])] = value

    def append_attribute(self, attribute):
        element = self.elements[-1]
        key = '.'.join(element['metadata_prefix'])
        if key not in element:
            element[key] = list()
        element[key].append(attribute)

    def skip_until_next_construct(self):
        count = 0
        while count > 0 or not self.tokenizer.peek_equals(RIGHT_PAREN):
            if self.tokenizer.peek_equals(LEFT_PAREN):
                count += 1
            elif self.tokenizer.peek_equals(RIGHT_PAREN):
                count -= 1
            self.tokenizer.next()

    def check_for_multiples(self, token, already_contains):
        if already_contains:
            raise RuntimeError(
                "Parse error: Multiple occurances of {}, near line {}".format(token, self.tokenizer.line_number))
        return True

    def expect_begin_construct(self):
        self.tokenizer.next()
        if LEFT_PAREN != self.tokenizer.token:
            self.tokenizer.expect(LEFT_PAREN)

    def not_end_construct(self):
        if RIGHT_PAREN != self.tokenizer.peek():
            return True
        return False

    def expect_end_construct(self):
        self.tokenizer.next()
        if RIGHT_PAREN != self.tokenizer.token:
            self.tokenizer.expect(RIGHT_PAREN)

    def expect(self, token):
        self.tokenizer.next()
        self.tokenizer.expect(token)

    def begin_construct(self):
        if LEFT_PAREN == self.tokenizer.peek():
            self.tokenizer.next()
            return True
        else:
            return False

    def construct_is(self, token):
        if self.tokenizer.peek_equals(token):
            return True
        return False


if __name__ == "__main__":
    # filename = r"C:\Users\keller\workplace\SpyDrNet\data\large_edif\osfbm.edf"
    filename = r"C:\Users\akeller9\workspace\SpyDrNet\data\large_edif\osfbm.edf"
    parser = EdifParser.from_filename(filename)
    import cProfile

    cProfile.run('parser.parse()')