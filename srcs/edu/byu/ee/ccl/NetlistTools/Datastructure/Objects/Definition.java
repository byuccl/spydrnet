package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifCell;
import edu.byu.ece.edif.core.EdifNet;
import edu.byu.ece.edif.core.EdifPort;
import edu.byu.ece.edif.core.PropertyList;

import java.util.ArrayList;
import java.util.List;

public class Definition extends NetlistObject {
    //List<PortDefinition> portDefinitions = new ArrayList<>();
    //List<BusDefinition> busDefinitions = new ArrayList<>();
    //List<Instance> instances = new ArrayList<>();
    //int definitionReference;
    List<Instance> instanceList = new ArrayList<>();
    List<Bus> busList = new ArrayList<>();
    List<Port> portList = new ArrayList<>();

    public Definition(EdifCell edifCell){
        super();
        setName(edifCell.getName());
        PropertyList propertyList = edifCell.getPropertyList();
        //TODO: need to convert the property list as a string
        insertMetadata("propertyList", "TODO: need to convert the property list as a string");
        if(propertyList != null){
            propertyList.forEach((k,v) -> insertMetadata(k,v.getValue().toString()));
        }
        //definition.linkLibrary(this);
        //edifCell.getPortRefs().forEach(edifPortRef -> insertPort(edifPortRef));
        edifCell.getNetList().forEach(edifNet -> insertBus(edifNet));
    }
//
////    public void linkLibrary(Library library){
////        this.library = library;
////    }
//
//    public void insertPort(EdifPort edifPort){
//        //Port portInstance = new Port(edifPort);
//        //portInstance.setName(edifPort.getName());
//        //ports.add(portInstance);
//        //portDefinitions.add(new PortDefinition(edifPort));
//    }
//
    public void insertBus(EdifNet edifNet){
        busList.add(new Bus(edifNet));
    }
//
//
//    public void linkInstance(){
//
//    }

    public void addInstance(Instance instance){
        instanceList.add(instance);
    }

    public void addBus(Bus bus){
        busList.add(bus);
    }

    public void addPort(Port port){
        portList.add(port);
    }

}
