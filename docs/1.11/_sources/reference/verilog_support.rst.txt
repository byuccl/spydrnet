Verilog Language Support
########################

Structural Verilog support has been added to SpyDrNet, and as of the 1.8.1 release has become much more stable. There are many constructs that are supported and some that aren't feel free to read through this to understand what Structural Verilog support means for SpyDrNet. 

If you need a new feature added to the verilog parser or composer feel free to let us know in an issue, with an example file (simplest possible that shows the issue) and the intended meaning. Otherwise feel free to fork add the feature and pull request to the SpyDrNet repository. As of version 1.8.1 our testing was done against verilog generated with Xilinx Vivado's write_verilog command in the tcl console. We would love to add more support for constructs written by other vendors, example netlists that fail help us out a ton!

Structural Verilog?
*******************

We use the terms Structural Verilog and Verilog netlists interchangeably for the most part. In a pure sense though, a Verilog netlist is a file that describes a netlist written in Structural Verilog, Structural verilog is in turn, a subset of Verilog that represents modules, instantiations, and the connections between these instances.

When parsing with SpyDrNet, more complex behavioral or datapath operations will cause an error or perhaps do something unexpected. The intermediate representation is intended to represent and modify netlists, and currently does not and likely never will have a sythesis step. Always blocks, if, case statements are some examples of things that will likely never be supported.

Terminology between Verilog and SpyDrNet
****************************************

Sturctural verilog and SpyDrNet have a similar structure. The following table is intended to help draw parallels between the two formats and let users get an idea of how they can expect their verilog netlists to show up in SpyDrNet

See the additional sections in the Supported Constructs for more information about how these are represented and maintained in SpyDrNet.

.. list-table:: Verilog vs SpyDrNet naming convention
   :widths: 50 50
   :header-rows: 1

   * - Verilog name/description
     - SpyDrNet name/description
   * - module
     - Definitionm
   * - wire/reg
     - Cable
   * - wire/reg index (bus[0])
     - Wire
   * - input/output/inout
     - Port
   * - module instantiation
     - Instance
   * - assign
     - instance (in and out connected)
   * - constraints "(\* const \*)"
     - metadata "VERILOG.InlineConstraints"
   * - parameters
     - metadata "VERILOG.Parameters"


Supported Constructs
********************

There are several features that are currently supported by the Verilog Parser and Composer pair

Ports
=====

Module declarations represent Definitions in SpyDrNet and are parsed as such. Inputs and outputs can be declared in the header in two main ways. Both are supported by SpyDrNet:

 
.. code-block:: verilog

   module module_name(
     input my_in,
     output [3:0] my_out);
 
or with just the names in the header
 
.. code-block:: verilog

   module module_name(
     my_in,
     my_out);
   input my_in;
   output [3:0] my_out;


Input output and inout are supported port directions.

When declared either way a SpyDrNet cable is created that will have the same name as the port. This cable is used to connect the ports to other modules instantiated in the module body. A notable exception exists. see the section on Port Remapping in Module headers

It is presumed that all of these ports are of type wire by default even if another default is declared by a preprocessor macro. See the section on preprocessor macros.

Ports are also listed when creating an instance. When creating an instance that was not previously defined with a module definition (no definition exists in the netlist yet), the parser will create a new definition with ports of undefined direction which defaults to inout on write. These ports will assume the minimum length needed to attach the cable defined in the definition. Later when the definition is found an update is made.

Currently there is not really a sanity check if the ports on an instance do not match up with the defined module. The port may end up larger if the widths do not match up.  The ports should not end up smaller than they are defined in the module though.

Wire/Reg, Module, Instatiations
===============================

Verilog Wire and Reg declarations are supported. These declarations will be converted to SpyDrNet cables. Modules are converted to SpyDrNet Definitions and instantiations will create SpyDrNet instances.

\`celldefine
============

The \`celldefine directive is used by SpyDrNet to know which modules are primitives. Most Vivado generated netlsits include a list of primitives that include simulation behavior. When the \`celldefine is encountered a primitive flag is set when the \`endcelldefine is encountered the flag is unset.

Any modules parsed while the primitive flag is set will ignore the module body and simply look for port information. Note that the keyword input output or inout in constructs similar to functions or tasks but not functions or tasks could cause issues. (the error will likely be, expected port name defined in the module header to declare a port with the name and line number) If this happens let us know what construct caused the problem and we can add a skip to it so that the keyword in these functions is ignored.

Assign
=======

Verilog's assign statement `assign output = input;` is supported if nothing other than a straight wire/reg to wire/reg assignment is happening. `&`, `|`, `^`, `+`, `-` ... and concatenations are currently not supported.

Internal to SpyDrNet Assignments are represented as instances with an in port out port and a single cable that connects the 2 ports. The value on the right hand side of the = is attached to the in port. The value on the left is attached to the out port. 

All Definitions representing various widths of assignments are stored in a library named SDN_VERILOG_ASSIGNMENT. The definitions generated with `"SDN_VERILOG_ASSIGNMENT_" + str(width)`
and the instances have the same name as the definitions with a `"_" + str(UID)` added to the end where UID is a counter that starts at 0 and counts up.

Assignment Defintions have two ports, `i` and `o`. the `i` port is input and attached to the cable on the right of the assignment while the `o` port is output, attached to the cable on the left hand side of the assignment.

The assignment instances are not written out to a verilog file in the same way other instances are, instead they are swapped out with an assign statement to mimic the original file.

Port Remapping in Module headers
================================

Vivado occasionally will write a verilog file with a construct in the module port declaration region that looks like the following.

.. code-block: verilog
   module b13
     (
       .canale({\canale[3] ,\canale[2] ,\canale[1] ,\canale[0] })
     ); 
   //module contents
   //the \ in the names is discussed in the escaped identifiers section


In SpyDrNet terminology,  the cable or wires (from multiple cables) in the concatenation are exclusively used internally, while the port name which is preceded by the . is used exclusively outside the module. In these cases, the port is created with the each of the wires listed in the concatenation attached to a pin on the port.

Currently only single bit breakouts are supported and having more than one bit in a cable in the concatenation will result in only the first bit being connected. The port is also assumed to have a width equal to the number of cables in the concatenation.

Parameters
==========

SpyDrNet currently supports parameters in the metadata. This allows users to parser, set and write parameters to and from Verilog Netlists. Parameters include essential information about instances and modules(SpyDrNet definitions)

These constructs are parsed into a dictionary that will be associated with a Definition or Instance. All constraints that are in the definition will not be automatically included in the instance. Instead constraints in the instances are generated independently and on a need basis.

Included are examples of good syntax for both module and instantiation parameters.

Module

.. code-block: verilog
   module my_module #(
     parameter Key = "VALUE",
     parameter Key2 = 8'h00
   )(
     input port_information_here
   );


Instantiation

.. code-block: verilog
   //LUT4 instantiation from our 4bitadder.v support file (some ports missing)
   LUT4 #(
     .INIT(16'hEC80)) //key is "INIT" and value is "16'hEC80"
     un3_answer1_p4
      (.I0(data11r[0]),
       ...
       .O(\^un3_answer1_p4 ));


The parameters on a parsed verilog file can be found in the metadata in instances and definitions as "VERILOG.Parameters" this stores a dictionary of all of the parameters that were included in the module (SpyDrNet Definition) or module instantiation (SpyDrNet instance). The key in the dictionary is to the left of the equal sign the text to the right of the equal sign is the value. These are always stored as strings even if the input data is numeric

There is currently no check to ensure that a constraint on an instance is actually on the module. The composer will write all constraints present to the file as though they are on the module too.


Inline Constraints
==================

SpyDrNet will parse and store Inline verilog constraints using the Vivado format. Below are examples of a few supported constraint constructs in verilog


``(* key = value *) //as a key value pair``

``(* no_value *) //as a single key``

``(* no_value, no_value_2, key = value *) //either or both of the above as a set``

All of these are supported ways of representing constraints. Multiple sets of constraints can exist before constructs. Currently, Modules, instantiations, wires/regs all allow for constraints to be defined. The constraints are unused in SpyDrNet but will be written on the compose step. When writing all constraints will be combined into a single set.

Constraints are included in Definitions, Instances and Cables in a dictionary that can be found in the meta dictionary with the key "VERILOG.InlineConstraints". All keys and values are strings.

Currently constraints from an XDC constraints file or other external file are not supported directly in the library. Users can add this functionality if desired. If you do add this functionality and want to share feel free to pull request or let us know in an issue.

Escaped Identifiers
===================

Occasionally a generated Verilog construct identifier will begin with a \ in these cases the name can contain any non-whitespace character. These names are always terminated with a whitespace character. internal to SpyDrNet the names include both the \ and the whitespace at the end this helps make composing simpler as the name can always be written as is.

Preprocessor Macros
===================

SpyDrNet does not currently have a preprocessor to handle defines and ifdef elseif endif etc. all of these constructs are skipped, from if to endif else is also skipped and ifndef is skipped as well. So putting your code in any of these constructs will cause the SpyDrNet parser to just skip it.

One notable exception to this rule is the \`celldefine and \`endcelldefine directives. These directives indicate that a module is a primitive module. See the section on \`celldefine

There is rudimentary support for storing the details of a \`timescale and other macros in the metadata for a definition. This is not tested well and may have some unexpected behavior. The composer ignores these constructs and they will not be written to the resulting file.

**Note to developers about macro handling :**
The tokenizer splits tokens beginning with \` into only two tokens even if the line has whitespace. example \`timescale 1 ps / 1 ps is split into a token of "\`timescale" and one of "1 ps / 1 ps" looking for the endline to end the second token. Single word directives will be one token.
