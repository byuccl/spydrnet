package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifCell;

import java.util.ArrayList;
import java.util.List;

public class Instance extends NetlistObject {

    int definitionReference;
    //List<Port> ports = new ArrayList<>();
    //List<Bus> buses = new ArrayList<>();
    //Environment environment;

    public Instance(Definition def){
        super();
        definitionReference = def.getUID();
    }

//    public Instance(EdifCell edifCell, Environment environment){
//        //edifCell.getPortList().forEach((c) -> ports.add(new Port(c)));
//        //edifCell.getNetList().forEach((n) -> buses.add(new Bus(n)));
//        environment.getDefinitionReference();
//    }
//
//
//    public void linkDefinition(Definition definition){
//        //if the definition is used already then we assign that number to this instance
//        //otherwise we need to create a new definition and assign it.
//        definitionReference = environment.getDefinitionReference(definition);
//    }
//
//
//    //the edif files we work with only have single bit ports?
//    //We will just keep that convention here.
//    public void insertPortInstances(){
//
//    }
}
