package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifNet;

public class BusDefinition extends NetlistObject {
    private int wireCount = 0;
    private int lowIndex = 0;
    private boolean isDownto = true;

    public BusDefinition(EdifNet edifNet){
        super();
        wireCount = 1;
        lowIndex = 0;
    }

    public void setWireCount(int wireCount){
        this.wireCount = wireCount;
    }

    public void setLowIndex(int lowIndex){
        this.lowIndex = lowIndex;
    }

    public void setIsDownto(boolean isDownto){
        this.isDownto = isDownto;
    }

    public int getWireCount(){
        return wireCount;
    }

    public int getLowIndex(){
        return lowIndex;
    }

    public boolean isDownto(){
        return isDownto;
    }

}
