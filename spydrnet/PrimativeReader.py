

class PrimativeReader:
    """Handle the input of primative cells into the tools"""
    def vivado(self, filein):
        r"""
        read from the file at path "filein" and return a primative library

        to create the file referenced by filein the following tcl commands
        must be run in vivado on an open design on the desired part number
        
        set fid [open "prim.txt" w]
        foreach c [get_lib_pins] {puts $fid $c\n[report_property -return_string $c]\n}
        close $fid

        The file generated will be located in C:\Users\username\AppData\Roaming\Xilinx\Vivado 
        or a similar location on windows. to override this just replace "prim.txt" with
        a full path to your desired file location.

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
                                    ....**
                                    }
                        ....
                        }
            ....
            }
        *I am not sure these signals are essential to the design. They seem to be constant values.
        **Other information may be available. this was written based on a 7 series device.

        """


        prim_lib = dict()

        with open(filein) as f:
            i = 0
            cell = None
            pin = None
            prop = dict()
            pos = None
            for line in f:
                if line == "\n":
                    prim_lib[cell] = dict()
                    prim_lib[cell][pin] = prop
                    prop = dict()
                    pin = None
                    cell = None
                    i = 0
                elif i == 0:
                    l = self._vivado_name_(line)
                    cell = l[0]
                    pin = l[1]
                    i = 1
                elif i == 1:
                    pos = self._vivado_header_(line)
                    i = 2
                elif i == 2:
                    l = self._vivado_property_(line, pos)
                    if l[1].lower() == "name":
                        if pin != l[1]:
                            print("The property name does not match the pin name from above...")
                            print(l[1] + " " + pin)
                    else:
                        prop[l[0]] = l[1]

        return prim_lib



    def _vivado_name_(self, line):
        """return the name of the cell and the pin"""
        l = line.split("/")
        if(len(l) > 2):
            print("something weird is going on here...too many '/' perhaps")
            print(l)
        return l
        

    def _vivado_header_(self, line):
        """Return the position of the property and value fields"""
        line = line.lower()
        l = line.split()
        return l.index("property"), l.index("value")


    def _vivado_property_(self, line, position):
        """
        return the key and value for each property

        Arguments:
        line        -   the string to be evaluated
        position    -   the return value from _vivado_header_ a ([pos_property, pos_value])
        """
        l = line.split()
        if(position[1] < len(l)):
            return l[position[0]], l[position[1]]
        else:
            return l[position[0]], ""


pr = PrimativeReader()
print(pr.vivado("prim.txt"))
