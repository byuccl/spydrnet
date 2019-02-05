package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifNet;
import edu.byu.ee.ccl.NetlistTools.Datastructure.Objects.Managers.ReferenceManager;

import java.util.*;

public class Wire extends NetlistObject {

    private List<Pin> pinList = new ArrayList<>();
//    private int referenceNumber;
//    private Set<Integer> pinReferenceList = new HashSet<>();
//
    public Wire(EdifNet edifNet){
        super();
        edifNet.getPortRefList().forEach(edifPortRef -> pinList.add(new Pin(edifPortRef.getSingleBitPort())));
    }
//
//    public void setReferenceNumber(int referenceNumber){
//        this.referenceNumber = referenceNumber;
//    }
//
//    public void insertPinRef(int pinReference){
//        pinReferenceList.add(pinReference);
//    }
//
//    public int getReferenceNumber(){
//        return referenceNumber;
//    }

}
