package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifPort;
import edu.byu.ece.edif.core.EdifPortRef;

public class PortDefinition extends NetlistObject {
    private int pinCount = 0;
    private int lowIndex = 0;
    private boolean isDownto = true;



    private static final String IN = "in";
    private static final String OUT = "out";
    private static final String INOUT = "inout";
    private static final String UNDEFINED = "undefined";

    private String direction = UNDEFINED;

    public PortDefinition(EdifPortRef edifPortRef){
        super();
        EdifPort edifPort = edifPortRef.getPort();
        pinCount = edifPort.getWidth();
        //convert from the old edif format to our new format using strings.
        switch(edifPort.getDirection()) {
            case 1:
                direction = IN;
                break;
            case 2:
                direction = OUT;
                break;
            case 3:
                direction = INOUT;
                break;
            default:
                direction = UNDEFINED;
                break;
        }
    }

    public void setPinCount(int pinCount) {
        this.pinCount = pinCount;
    }
}
