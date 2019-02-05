package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifPortRef;
import edu.byu.ece.edif.core.EdifSingleBitPort;

public class Pin extends NetlistObject{
    public int bitPosition;

    public Pin(EdifSingleBitPort edifSingleBitPort){
        super();
        bitPosition = edifSingleBitPort.bitPosition();
        setName(edifSingleBitPort.getPortName() + " " + bitPosition);
    }
}
