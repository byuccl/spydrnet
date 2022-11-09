Callback Framework
##################

SpyDrNet features a callback framework that allows developers to create plugins to watch a netlist data structure and register actions when certain changes are made. The callback framework was used to implement a namespace manager as a proof of concept. It could be used to implement additional design rule checks, a modification history log, or similar netlist watching features.

Watched features
****************

the following table illustrates the currently implemented capabilities.


* N - Netlist
* L - Library
* D - Definition
* P - Port
* C - Cable
* I - Instance
* W - Wire
* p - Pin \*

\* currently the pins do not have any callbacks implemented

.. list-table:: Watched API Methods
   :widths: 33 33 34
   :header-rows: 1

   * - Feature
     - Watched Classes
     - Parameters
   * - Creation
     - NLDPCIW--
     - Created object
   * - Add/Remove Wire
     - ----C---
     - cable, wire
   * - Add/Remove Port
     - --D-----
     - definition, port
   * - Add/Remove Child
     - --D-----
     - definition, child
   * - Add/Remove Cable
     - --D-----
     - definition, cable
   * - Modify Reference
     - -----I--
     - instance, reference
   * - Add/Remove Definition
     - -L------
     - netlist, instance
   * - Add/Remove Netlist
     - N-------
     - netlist, library
   * - Add/Remove Pin
     - ---P----
     - port, pin
   * - Connect/Disconnect Pin
     - ------W-
     - wire, pin
   * - Set/Delete/Pop metadata
     - NLDPCIW--
     - element (object), key

The feature column lists the function/behavior that is watched for. The "Watched SpyDrNet Classes" column highlights the SpyDrNet class on which the feature is watched. The parameters column lists the objects that are passed back.

Implementation
**************

Implementing a call back listner involves creating a class that inherits and overrides from the existing CallbackListener class. Each of the desired methods will need to be overwritten in the inheriting class.

Callbacks are made after sanity checks but before modifications are made to the datastructure. This allows users of the callback framework to prevent unwanted changes from taking place. This is an advantage in cases where an error can be detected before it is applied. Additional callbacks after the application of changes to the datastructure are currently not implemented to try keep the data structure light weight and quicker.

Users of the callback feature must take into account that other users of the callbacks may later deny the modification. The order in which the callbacks are registered should match the order in which the callbacks are made. If it is important that the method succeeds after the callback is made, ensure that that callback listener is registered last or at least not before other callbacks that may prevent the proposed action.

Additionally, since callbacks are made from within the API itself, be cautious when making API calls from within a callback. Infinite loops could be created.
