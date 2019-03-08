

class PrimativeReader:
    """Handle the input of primative cells into the tools"""
    def vivado(self, filein):
        """
        read from the file at path "filein" and return a primative library

        to create the file referenced by filein the following tcl commands
        must be run in vivado on an open design on the desired part number
        
        set fid [open "prim.txt" w]
        foreach c [get_lib_pins] {puts $fid $c\n[report_property -return_string $c]\n}
        close $fid

        Argument:
        filein -- the path to the file from which to read the vivado output
        
        Return:
        A dictionary of dictionaries conforming with the following example
            {CellName : {PinName : {CLASS       : lib_pin*
                                    DIRECTION   : input/output
                                    FUNCTION    : ""*
                                    IS_CLEAR    : 0/1
                                    IS_CLOCK    : 0/1
                                    IS_DATA     : 0/1
                                    IS_SETRESET : 0/1
                                    }
                        ....
                        }
            ....
            }
        *I am not sure these signals are essential to the design. They seem to be constant values.

        """
        pass
