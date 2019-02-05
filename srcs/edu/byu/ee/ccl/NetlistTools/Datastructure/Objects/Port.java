package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifPort;
import edu.byu.ece.edif.core.EdifPortRef;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Port extends NetlistObject{
    int portDefinitionReference;
    List<Pin> pins = new ArrayList<>();
    Direction direction;

    Port(EdifPort edifPort){
        super();
        //make a function here that steals the name add metadata later.
        setName(edifPort.getName());
    }

    //public Port(/*EdifPort oldPort*/) {
        //copy properties of port (width, direction, etc.)
        //squiggle
    //}

    //Port(EdifPortRef edifPortRef){
    //    EdifPort edifPort = edifPortRef.getPort();
    //    edifPortRef.getNet();
    //    edifPortRef.getCellInstance();
    //    edifPortRef.getSingleBitPort();
    //}


    public void addPin(Pin pin){
        pins.add(pin);
    }

    //public void insertPin(int pinRef){
    //    //pinRefList.add(pinRef);
    //}
}
