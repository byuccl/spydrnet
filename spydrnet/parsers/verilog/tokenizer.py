#Copyright 2020 Please see the license
#Author Dallin Skouson

class verilog_tokenizer:
    '''
    Can tokenize a verilog file. That's all it does.
    
    initialize with the file path
    call next to get the next token in the verilog file.
    '''

    # The following basic tokens are in a verilog file.
    # whitespace (just skipped and not returned)
    # ` directives
    # ;
    # (* SOMEDIRECTIVE = "some string" *)
    # input
    # output
    # inout
    # wire
    # reg?
    # variable name
    # #
    # [number:number]
    # assign
    # parameter
    # pulldown
    # not
    # and

    # let's tokenize!

    __slots__ = ["_file_stream"]

    def __init__(self, file_path):
        '''open the file located at file_path'''
        f = open(file_path)

    def next(self):
        '''read in the next token and return it
        if no more tokens are available return eof and close the file.'''
        pass