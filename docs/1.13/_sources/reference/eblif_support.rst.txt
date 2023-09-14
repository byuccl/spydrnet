.. _eblif_support:

EBLIF Support
--------------

SpyDrNet's EBLIF parser requires/follows conventions followed by Symbiflow. Only structural BLIF is supported, as well as a few extensions (EBLIF). See Symbiflow's File Format page (https://docs.verilogtorouting.org/en/latest/vpr/file_formats/#vpr-pack-file) for more details. It is important to point out that, along with Symbiflow's VPR, SpyDrNet expects designs in the EBLIF format to be flat. Hierarchy is not currently supported by either.

In addition, it is important that .blackbox modules are included in the netlist to provide SpyDrNet with the information about primitives in the netlist (port directions, etc.).
