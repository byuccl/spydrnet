from spydrnet.parsers.edif.tokenizer import EdifTokenizer
from spydrnet.ir import *
from spydrnet.parsers.edif.edif_tokens import *

import itertools

class Design:
    pass

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

        self.parse_construct(self.parse_edif)

    def initialize_tokenizer(self):
        self.tokenizer = EdifTokenizer.from_filename(self.filename)

    def parse_edif(self):
        self.elements.append(Environment())
        self.expect(EDIF)
        self.parse_nameDef()
        self.parse_header()
        self.parse_body()
        return self.elements.pop()

    def parse_header(self):        
        self.parse_construct(self.parse_edifVersion)
        self.parse_construct(self.parse_edifLevel)
        self.parse_construct(self.parse_keywordMap)

    def parse_edifVersion(self):
        self.expect(EDIF_VERSION)
        version_0 = self.parse_integerToken()
        version_1 = self.parse_integerToken()
        version_2 = self.parse_integerToken()

        self.set_attribute('EDIF.version', (version_0, version_1, version_2))

    def parse_edifLevel(self):
        self.expect(EDIF_LEVEL)
        level = self.parse_integerToken()
        self.set_attribute('EDIF.level', level)

    def parse_keywordMap(self):
        self.expect(KEYWORD_MAP)
        self.parse_construct(self.parse_keywordLevel)

        while self.begin_construct():
            self.parse_construct(self.parse_comment)

    def parse_keywordLevel(self):
        self.expect(KEYWORD_LEVEL)
        level = self.parse_integerToken()
        self.set_attribute('EDIF.keywordLevel', level)

    def parse_body(self):
        has_status = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()

            elif self.construct_is(EXTERNAL): self.parse_library()
            elif self.construct_is(LIBRARY): self.parse_library()
            elif self.construct_is(DESIGN): self.parse_design()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect("|".join([STATUS, EXTERNAL, LIBRARY, DESIGN, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_status(self):
        self.expect(STATUS)
        while self.begin_construct():
            if self.construct_is(WRITTEN): self.parse_written()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect("|".join([WRITTEN|COMMENT|USER_DATA]))
            self.expect_end_construct()

    def parse_written(self):
        self.expect(WRITTEN)
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

            elif self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect("|".join([AUTHOR, PROGRAM, DATA_ORIGIN, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_timeStamp(self):
        self.expect(TIME_STAMP)
        year = self.parse_integerToken()
        month = self.parse_integerToken()
        day = self.parse_integerToken()
        hour = self.parse_integerToken()
        minute = self.parse_integerToken()
        sec = self.parse_integerToken()

    def parse_author(self):
        self.expect(AUTHOR)
        author = self.parse_stringToken()
        self.set_attribute('EDIF.author', author)

    def parse_program(self):
        self.expect(PROGRAM)
        program = self.parse_stringToken()
        self.set_attribute('EDIF.program', program)
        
        if self.begin_construct():
            self.expect(VERSION)
            version = self.parse_stringToken()
            self.set_attribute('EDIF.program.version', version)
            self.expect_end_construct()

    def parse_library(self):
        self.elements.append(Library())
        
        self.expect(LIBRARY)
        self.parse_nameDef()
        self.parse_construct(self.parse_edifLevel)
        self.parse_construct(self.parse_technology)

        has_status = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()

            elif self.construct_is(CELL): self.parse_cell()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect("|".join([STATUS, CELL, COMMENT, USER_DATA]))
            self.expect_end_construct()

        return self.elements.pop()

    def parse_technology(self):
        self.expect(TECHNOLOGY)
        self.parse_construct(self.parse_numberDefinition)

    def parse_numberDefinition(self):
        self.expect(NUMBER_DEFINITION)
        while self.begin_construct():
            raise NotImplementedError()
            self.expect_end_construct()

    def parse_cell(self):
        self.elements.append(Definition())

        self.expect(CELL)
        self.parse_nameDef()
        self.parse_construct(self.parse_cellType)

        has_status = False
        has_viewMap = False
        while self.begin_construct():
            if self.construct_is(STATUS):
                has_status = self.check_for_multiples(STATUS, has_status)
                self.parse_status()
            
            elif self.construct_is(VIEW): self.parse_view()
            elif self.construct_is(VIEW_MAP):
                has_viewMap = self.check_for_multiples(VIEW_MAP, has_viewMap)
                self.parse_viewMap()

            elif self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([STATUS, VIEW, VIEW_MAP, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

        return self.elements.pop()

    def parse_cellType(self):
        self.expect(CELL_TYPE)
        if self.construct_is(GENERIC): self.tokenizer.next()
        elif self.construct_is(TIE): self.tokenizer.next()
        elif self.construct_is(RIPPER): self.tokenizer.next()
        else: self.expect("|".join([GENERIC, TIE, RIPPER]))

    def parse_view(self):
        self.expect(VIEW)
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

            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([STATUS, CONTENTS, COMMENT, PROPERTY, USER_DATA]))
            self.expect_end_construct()

    def parse_viewType(self):
        self.expect(VIEW_TYPE)
        if self.construct_is(BEHAVIOR): self.tokenizer.next()
        elif self.construct_is(DOCUMENT): self.tokenizer.next()
        elif self.construct_is(GRAPHIC): self.tokenizer.next()
        elif self.construct_is(LOGICMODEL): self.tokenizer.next()
        elif self.construct_is(MASKLAYOUT): self.tokenizer.next()
        elif self.construct_is(NETLIST): self.tokenizer.next()
        elif self.construct_is(PCBLAYOUT): self.tokenizer.next()
        elif self.construct_is(SCHEMATIC): self.tokenizer.next()
        elif self.construct_is(STRANGER): self.tokenizer.next()
        elif self.construct_is(SYMBOLIC): self.tokenizer.next()
        else: self.expect("|".join([BEHAVIOR, DOCUMENT, GRAPHIC, LOGICMODEL, MASKLAYOUT, NETLIST, PCBLAYOUT, SCHEMATIC, STRANGER, SYMBOLIC]))

    def parse_interface(self):
        self.expect(INTERFACE)
        while self.begin_construct():
            if self.construct_is(PORT): self.parse_port()

            elif self.construct_is(PORT_BUNDLE): raise NotImplementedError()
            elif self.construct_is(SYMBOL): raise NotImplementedError()
            elif self.construct_is(PROTECTION_FRAME): raise NotImplementedError()
            elif self.construct_is(ARRAY_RELATED_INFO): raise NotImplementedError()
            elif self.construct_is(PARAMETER): raise NotImplementedError()
            elif self.construct_is(JOINED): raise NotImplementedError()
            elif self.construct_is(MUST_JOIN): raise NotImplementedError()
            elif self.construct_is(WEAK_JOINED): raise NotImplementedError()
            elif self.construct_is(PERMUTABLE): raise NotImplementedError()
            elif self.construct_is(TIMING): raise NotImplementedError()
            elif self.construct_is(SIMULATE): raise NotImplementedError()
            elif self.construct_is(DESIGNATOR): raise NotImplementedError()
            elif self.construct_is(WEAK_JOINED): raise NotImplementedError()

            elif self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([PORT, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_port(self):
        self.expect(PORT)
        if self.begin_construct():
            if self.construct_is(RENAME): self.parse_rename()
            elif self.construct_is(ARRAY): self.parse_array()
            else: self.expect('|'.join([RENAME, ARRAY]))
            self.expect_end_construct()
        else: self.parse_nameDef()

        has_direction = False
        while self.begin_construct():
            if self.construct_is(DIRECTION):
                has_direction = self.check_for_multiples(DIRECTION, has_direction)
                self.parse_direction()

            elif self.construct_is(UNUSED): raise NotImplementedError()
            elif self.construct_is(DESIGNATOR): raise NotImplementedError()
            elif self.construct_is(DC_FANIN_LOAD): raise NotImplementedError()
            elif self.construct_is(DC_FANOUT_LOAD): raise NotImplementedError()
            elif self.construct_is(DC_MAX_FANIN): raise NotImplementedError()
            elif self.construct_is(DC_MAX_FANOUT): raise NotImplementedError()
            elif self.construct_is(AC_LOAD): raise NotImplementedError()
            elif self.construct_is(PORT_DELAY): raise NotImplementedError()

            elif self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([DIRECTION, PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_array(self):
        self.expect(ARRAY)
        self.parse_nameDef()
        self.parse_integerToken()
        while self.tokenizer.is_valid_identifier():
            self.parse_integerToken()

    def parse_direction(self):
        self.expect(DIRECTION)
        if self.construct_is(INOUT): self.tokenizer.next()
        elif self.construct_is(INPUT): self.tokenizer.next()
        elif self.construct_is(OUTPUT): self.tokenizer.next()
        else: self.expect('|'.join([INOUT, INPUT, OUTPUT]))

    def parse_contents(self):
        self.expect(CONTENTS)
        while self.begin_construct():
            if self.construct_is(INSTANCE): self.parse_instance()
            elif self.construct_is(NET): self.parse_net()

            elif self.construct_is(OFF_PAGE_CONNECTOR): raise NotImplementedError()
            elif self.construct_is(FIGURE): raise NotImplementedError()
            elif self.construct_is(SECTION): raise NotImplementedError()
            elif self.construct_is(NET_BUNDLE): raise NotImplementedError()
            elif self.construct_is(PAGE): raise NotImplementedError()
            elif self.construct_is(COMMENT_GRAPHICS): raise NotImplementedError()
            elif self.construct_is(PORT_IMPLEMENTATION): raise NotImplementedError()
            elif self.construct_is(TIMING): raise NotImplementedError()
            elif self.construct_is(SIMULATE): raise NotImplementedError()
            elif self.construct_is(WHEN): raise NotImplementedError()
            elif self.construct_is(FOLLOW): raise NotImplementedError()
            elif self.construct_is(LOGIC_PORT): raise NotImplementedError()
            elif self.construct_is(BOUNDING_BOX): raise NotImplementedError()
            elif self.construct_is(TIMING): raise NotImplementedError()
            
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([INSTANCE, NET, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_instance(self):
        self.expect(INSTANCE)
        self.parse_nameDef()
        if self.begin_construct():
            if self.construct_is(VIEW_REF): self.parse_viewRef()
            elif self.construct_is(VIEW_LIST): raise NotImplementedError()
            else: self.expect(VIEW_REF)
            self.expect_end_construct()

        while self.begin_construct():
            if self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()

    def parse_viewRef(self):
        self.expect(VIEW_REF)
        self.parse_nameRef()
        if self.begin_construct():
            self.parse_cellRef()
            self.expect_end_construct()

    def parse_cellRef(self):
        self.expect(CELL_REF)
        self.parse_nameDef()
        if self.begin_construct():
            self.parse_libraryRef()
            self.expect_end_construct()

    def parse_libraryRef(self):
        self.expect(LIBRARY_REF)
        self.parse_nameDef()

    def parse_net(self):
        self.expect(NET)
        self.parse_nameDef()
        self.parse_construct(self.parse_joined)

        while self.begin_construct():
            if self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            elif self.construct_is(USER_DATA): self.parse_userData()
            else: self.expect('|'.join([PROPERTY, COMMENT, USER_DATA]))
            self.expect_end_construct()
    
    def parse_joined(self):
        self.expect(JOINED)
        while self.begin_construct():
            if self.construct_is(PORT_REF): self.parse_portRef()
            elif self.construct_is(PORT_LIST): raise NotImplementedError()
            elif self.construct_is(GLOBAL_PORT_REF): raise NotImplementedError()
            else: self.expect(PORT_REF)
            self.expect_end_construct()

    def parse_portRef(self):
        self.expect(PORT_REF)
        if self.begin_construct():
            self.parse_member()
            self.expect_end_construct()
        else:
            self.parse_nameRef()
        
        while self.begin_construct():
            if self.construct_is(PORT_REF): raise NotImplementedError()
            elif self.construct_is(INSTANCE_REF): self.parse_instanceRef()
            elif self.construct_is(VIEW_REF): raise NotImplementedError()
            self.expect_end_construct()

    def parse_instanceRef(self):
        self.expect(INSTANCE_REF)
        if self.begin_construct():
            self.parse_member()
            self.expect_end_construct()
        else:
            self.parse_nameRef()


    def parse_member(self):
        self.expect(MEMBER)
        self.parse_nameDef()
        self.parse_integerToken()
        while self.not_end_construct():
            self.parse_integerToken()
            self.expect_end_construct()
    
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
        self.expect(COMMENT)
        while self.not_end_construct():
            comment = self.parse_stringToken()

    def parse_property(self):
        self.expect(PROPERTY)
        self.parse_nameDef()

        self.parse_construct(self.parse_typedValue)

        has_owner = False
        has_unit = False
        while self.begin_construct():
            if self.construct_is(OWNER):
                has_owner = self.check_for_multiples(OWNER, has_owner)
                self.parse_owner()

            elif self.construct_is(UNIT):
                has_unit = self.check_for_multiples(UNIT, has_unit)
                self.parse_unit()

            elif self.construct_is(PROPERTY): self.parse_property()
            elif self.construct_is(COMMENT): self.parse_comment()
            self.expect_end_construct()

    def parse_typedValue(self):
        if self.construct_is(BOOLEAN): self.parse_boolean()
        elif self.construct_is(INTEGER): self.parse_integer()
        elif self.construct_is(MI_NO_MAX): raise NotImplementedError()
        elif self.construct_is(NUMBER): self.parse_number()
        elif self.construct_is(POINT): raise NotImplementedError()
        elif self.construct_is(STRING): self.parse_string()
        else: self.expect('|'.join([BOOLEAN, INTEGER, NUMBER, STRING]))

    def parse_boolean(self):
        self.expect(BOOLEAN)
        self.expect_begin_construct()
        self.tokenizer.next()
        if self.tokenizer.token_equals(TRUE): result = True
        elif self.tokenizer.token_equals(FALSE): result = False
        else: self.expect('|'.join([TRUE, FALSE]))
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
        result = mantissa*10.0**exponent
        return result

    def parse_string(self):
        self.expect(STRING)
        self.parse_stringToken()

    def parse_owner(self):
        raise NotImplementedError()

    def parse_unit(self):
        raise NotImplementedError()

    def parse_nameRef(self):
        self.set_attribute('EDIF.identifier', self.parse_identifier())

    def parse_nameDef(self):
        if self.begin_construct():
            self.parse_rename()
            self.expect_end_construct()
        else:
            self.set_attribute('EDIF.identifier', self.parse_identifier())

    def parse_rename(self):
        self.expect(RENAME)
        self.set_attribute('EDIF.identifier', self.parse_identifier())
        self.set_attribute('EDIF.original_identifier', self.parse_stringToken())

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

    def set_attribute(self, key, value):
        element = self.elements[-1]
        element.set_entry(key, value)

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
            raise RuntimeError("Parse error: Multiple occurances of {}, near line {}".format(token, self.tokenizer.line_number))
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