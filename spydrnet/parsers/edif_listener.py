from spydrnet.ir import *

class EdifListener:
    def __init__(self):
        self.elements = list()
        self.identifiers = list()
        self.stringTokens = list()

    def enter_edif(self):
        print("Create environment")
        environment = Environment()
        self.elements.append(environment)

    def enter_nameDef(self):
        print("Enter nameDef")

    def exit_nameDef(self):
        identfier = self.identifiers.pop()
        if 
        print("Exit nameDef")

    def exit_edif(self):
        print("Finish enviroment")

    def push_identifier(self, identifier):
        self.identifiers.append(identifier)

    def push_stringToken(self, stringToken):
        self.stringTokens.append(stringToken)