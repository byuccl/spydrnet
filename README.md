# SpyDrNet
A flexible framework for analyzing and transforming netlists written in python and built to fill an important gap in FPGA research and reliability.

# A brief history
The BYU Configurable Computing lab has maintained BYU's edif tools for several years. These tools were tied to the EDIF format and were written in an older version of java. The idea was born for a tool that would not be locked to any vendor that would allow simple analysis and modification of netlists. After hours of research on how to generalize netlists and store them in a language agnostic format a prototype was developed in python. This prototype soon became useful in the lab for netlist analysis and reliability transformation studies. A more mature (though still having room for growth) tool is what we present here. 

We have tried to build this tool around the principles of expandability and modularity. Care has been taken to separate different parts of the program in an organized fashion.


# How to install
There are generally 2 options for installation. You can install from source from this repository, or install from pip. Both are explained here.

From pip
pip3 install SpyDrNet

From Source
TODO fill in instructions on how to install

Without Installing
Just extract/pull this folder in the same directory as the code that you wish to write. The structure should allow for import SpyDrNet from code written in that folder.

# How to contribute
If this tool has helped you out or you have new feature ideas that you would like to implement feel free to make a pull requrest, or take a look at the issues to see how to contribute. New ideas, bug fixes and suggestions are also welcome.

# Future Work

For the release:
We need good API examples
Complete API, object removal
We need good documentation

Prerelease for before the holidays

- check the projects tab on github for some information on this.
- we need to define the documentation pre-release as well.

We need a release check

1.1.0
new formats
merge netlists
constraint handling

Serializer of the itermediate representation look into pickle (for now) and json
Properties and names need work
callbacks
property management 

EDIF parser rework to use the creation API
EDIF composer rework to use the analysis API

Add plugin capability. - this should probably be discussed more with nailed down details.
