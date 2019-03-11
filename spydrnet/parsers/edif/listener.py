from spydrnet.ir import *

DEBUG = True

class EdifListener:
    def __init__(self):
        self.parser = None
        self.elements = list()
        self.identifiers = list()
        self.stringTokens = list()
        self.integerTokens = list()

        self.bookmarks = list()

    def enter_edif(self):
        if DEBUG: print("Object: edif")
        environment = Environment()
        self.elements.append(environment)

    def enter_edifVersion(self):
        self.integerTokens.clear()

    def exit_edifVersion(self):
        version_2 = self.integerTokens.pop()
        version_1 = self.integerTokens.pop()
        version_0 = self.integerTokens.pop()
        version = (version_0, version_1, version_2)
        if version != ("2", "0", "0"):
            raise RuntimeError("Parse error: Only EDIF Version 2 0 0 is supported, EDIF Version is {} {} {} on line {}".format(
                version_0, version_1, version_2, self.parser.line_number
            ))

        element = self.elements[-1]
        element.set_entry("EDIF.version", version)
        if DEBUG: print("version:", version_0, version_1, version_2)

        assert (not self.integerTokens)

    def enter_keywordMap(self):
        keywordMap = Element()
        self.elements.append(keywordMap)

    def enter_keywordLevel(self):
        self.integerTokens.clear()

    def exit_keywordLevel(self):
        keywordLevel = self.integerTokens.pop()
        
        element = self.elements[-1]
        element.set_entry("EDIF.keywordLevel", keywordLevel)
        if DEBUG: print("keywordLevel:", keywordLevel)
        
        assert (not self.integerTokens)

    def exit_keywordMap(self):
        keywordMap = self.elements.pop()
        keywordLevel = keywordMap.get_value("EDIF.keywordLevel")
        element = self.elements[-1]
        element.set_entry("EDIF.keywordMap.keywordLevel", keywordLevel)

        comments = keywordMap.get_value('comments')
        if comments:
            element.set_entry("EDIF.keywordMap.comments", comments)

    def enter_status(self):
        status = Element()
        self.elements.append(status)

    def enter_written(self):
        written = Element()
        self.elements.append(written)

    def enter_timestamp(self):
        self.integerTokens.clear()

    def exit_timestamp(self):
        
        second = self.integerTokens.pop()
        minute = self.integerTokens.pop()
        hour = self.integerTokens.pop()
        day = self.integerTokens.pop()
        month = self.integerTokens.pop()
        year = self.integerTokens.pop()
        timestamp = (year, month, day, hour, minute, second)

        element = self.elements[-1]
        element.set_entry("timestamp", timestamp)
        if DEBUG: print("timestamp:", timestamp)
        
        assert (not self.integerTokens)

    def enter_program(self):
        program = Element()
        self.elements.append(program)

    def enter_version(self):
        pass

    def exit_version(self):
        version = self.stringTokens.pop()
        element = self.elements[-1]
        element.set_entry("version", version)
        
    def exit_program(self):
        program = self.elements.pop()
        element = self.elements[-1]
        program_name = self.stringTokens.pop()
        element.set_entry("program", program_name)
        
        version = program.get_value('version')
        if version:
            element.set_entry("program.version", version)

    def enter_comment(self):
        self.bookmarks.append(len(self.stringTokens))

    def exit_comment(self):
        bookmark = self.bookmarks.pop()
        strings = self.stringTokens[bookmark:]
        self.stringTokens = self.stringTokens[:bookmark]
        if len(strings) > 0:

            element = self.elements[-1]
            if 'comments' not in element.data:
                element.set_entry('comments', list())
            element.get_value('comments').append((*strings,))
        if DEBUG: print("comment:", (*strings,))

    def exit_written(self):
        written = self.elements.pop()
        element = self.elements[-1]
        #TODO making assumption that only one written exists
        for key, value in written.data.items():
            element.set_entry("written." + key, value)

    def exit_status(self):
        status = self.elements.pop()

        element = self.elements[-1]
        for key, value in status.data.items():
            element.set_entry("EDIF.status." + key, value)

    def enter_edifLevel(self):
        self.integerTokens.clear()
    
    def exit_edifLevel(self):
        level = self.integerTokens.pop()

        element = self.elements[-1]
        element.set_entry("EDIF.level", level)
        if DEBUG: print("level:", level)

        assert (not self.integerTokens)

    def enter_library(self):
        pass
    
    def exit_library(self):
        pass

    def enter_cell(self):  
        pass

    def exit_cell(self):
        pass

    def enter_view(self):
        pass

    def exit_view(self):
        pass
    
    def enter_interface(self):
        pass

    def exit_interface(self):
        pass

    def enter_port(self):
        pass

    def exit_port(self):
        pass

    def enter_content(self):
        pass

    def exit_content(self):
        pass

    def enter_instance(self):
        pass

    def exit_instance(self):
        pass

    def enter_net(self):
        pass

    def exit_net(self):
        pass

    def enter_nameDef(self):
        self.identifiers.clear()
        self.stringTokens.clear()

    def exit_nameDef(self):
        element = self.elements[-1]
        
        edif_identifier = self.identifiers.pop()
        element.set_entry("EDIF.identifier", edif_identifier)
        if DEBUG: print("identifer:", edif_identifier)
        assert(not self.identifiers)
        
        if self.stringTokens:
            external_identifier = self.stringTokens.pop()
            element.set_entry("EDIF.external_identifier", external_identifier)
            if DEBUG: print("external identifer:", edif_identifier)
            assert(not self.stringTokens)

    def exit_edif(self):
        print("Finish enviroment")

    def push_identifier(self, identifier):
        self.identifiers.append(identifier)

    def push_stringToken(self, stringToken):
        self.stringTokens.append(stringToken)

    def push_integerToken(self, integerToken):
        self.integerTokens.append(integerToken)