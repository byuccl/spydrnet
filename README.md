# SpyDrNet
A flexible framework for analyzing and transforming netlists written in python and built to fill an important gap in FPGA research and reliability.

# A brief history
The BYU Configurable Computing lab has maintained BYU's edif tools for several years. These tools were tied to the EDIF format and were written in an older version of java. The idea was born for a tool that would not be locked to any vendor that would allow simple analysis and modification of netlists. After hours of research on how to generalize netlists and store them in a language agnostic format a prototype was developed in python. This prototype soon became useful in the lab for netlist analysis and reliability transformation studies. A more mature (though still having room for growth) tool is what we present here. Contributions in the form of bug reports, pull requests, and suggestions is always welcome.

# How to install
There are generally 2 options for installation. You can install from source from this repository, or install from pip. Both are explained here.

From pip

From Source

# How to contribute

# Future Work

Serializer of the itermediate representation look into pickle (for now) and json
Properties and names need work
callbacks
property management 

EDIF parser rework to use the creation API
EDIF composer rework to use the analysis API

Add plugin capability. - this should probably be discussed more with nailed down details.
