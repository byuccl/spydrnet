package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.*;
import edu.byu.ece.edif.util.parse.EdifParser;
import edu.byu.ece.edif.util.parse.ParseException;

import java.io.FileNotFoundException;
import java.util.*;

public class Traverse {
    EdifEnvironment oldNetlist;

    private static Map<EdifCell, Definition> cellDefinitionMap = new HashMap<>();

    /**
     * Reads in an EDIF file.
     * @param filename the name of the file that will be read in. Must be in EDIF format.
     */
    public void readNetlistFile(String filename) {
        try {
            oldNetlist = EdifParser.translate(filename);
        } catch (ParseException e) {
            System.out.println("[ERROR] Failed to parse EDIF.");
            e.printStackTrace();
            System.exit(-1);
        } catch (FileNotFoundException e) {
            System.out.println("[ERROR] File " + filename + " not found.");
            e.printStackTrace();
        }
    }

    public static Environment EnvironmentOut;

    public static void Main(String[] args) {
        Traverse traverse = new Traverse();
        traverse.readNetlistFile("C:\\Users\\ecestudent\\Desktop\\temp.edf");
        Environment newEnvironment = convertOldEnvironment(traverse.oldNetlist);
        EnvironmentOut = newEnvironment;
    }


    private static Environment convertOldEnvironment(EdifEnvironment oldNetlist){
        Environment environment = new Environment(oldNetlist);

        List<EdifLibrary> libraries = oldNetlist.getLibraryManager().getValidLibraryOrder();
        for (EdifLibrary oldLibrary : libraries) {
            Library newLibrary = convertOldLibrary(oldLibrary);
            environment.addLibrary(newLibrary);
        }
        return environment;
    }


    private static Library convertOldLibrary(EdifLibrary oldLibrary) {
        Library library = new Library(oldLibrary);

        for (EdifCell oldCell : oldLibrary.getValidCellOrder()) {
            Definition newDefinition;
            newDefinition = convertCell2Definition(oldCell);
            library.addDefinition(newDefinition);
        }
        return library;
    }

    private static Bus addEdifNetToBus(Map<String, Bus> busMap, EdifNet oldNet){
        String oldName = oldNet.getOldName();
        String busName;
        int bracketIndex = oldName.lastIndexOf('[');
        Bus busToAddWire;
        int bracketIndexClose = oldName.indexOf(']',bracketIndex);
        int position = 0;
        if (bracketIndex == -1) {
            busName = oldName;
            busToAddWire = new Bus(busName);
            busMap.put(busName,busToAddWire);
        } else {
            busName = oldName.substring(0,bracketIndex) + oldName.substring(bracketIndexClose+1);
            if(busMap.containsKey(busName)){

                busToAddWire = busMap.get(busName);
            }
            else{
                busToAddWire = new Bus(busName);
                busMap.put(busName,busToAddWire);
            }
        }
        busToAddWire.addWire(new Wire(oldNet));
        return busToAddWire;
    }


    private static void addNetsToDefinition(Definition definition, EdifCell oldCell){
        Map<String, Bus> busMap = new HashMap<>();
        for(EdifNet oldNet : oldCell.getNetList()){
            Bus newBus = addEdifNetToBus(busMap, oldNet);
        }
        busMap.forEach((k,b)->definition.addBus(b));
    }

    private static Map<EdifCellInstance, Set<Pin>> addPinsToPorts(Map<EdifPort, Port> portMap, EdifCell oldCell){
        Map<EdifCellInstance, Set<Pin>> instancePinMap= new HashMap<>();
        for(EdifNet oldNet : oldCell.getNetList()){
            for(EdifPortRef epr : oldNet.getPortRefList()){
                EdifCellInstance cellInstance = epr.getCellInstance();
                Pin pin = new Pin(epr.getSingleBitPort());
                if(cellInstance == null) {
                    portMap.get(epr.getPort()).addPin(pin);
                }
                else {
                    if(!instancePinMap.containsKey(cellInstance)) {
                        Set<Pin> pins = new HashSet<>();
                        instancePinMap.put(cellInstance, pins);
                    }
                    instancePinMap.get(cellInstance).add(pin);
                }
            }
        }
        return instancePinMap;
    }

    private static Definition convertCell2Definition(EdifCell oldCell) {
            Definition newDefinition = new Definition(oldCell);
            cellDefinitionMap.put(oldCell, newDefinition);
            addNetsToDefinition(newDefinition, oldCell);

            Map<EdifPort, Port> portMap = addPortsToDefinition(oldCell, newDefinition);

            Map<EdifCellInstance, Set<Pin>> instancePinMap = addPinsToPorts(portMap, oldCell);
            Collection<EdifCellInstance> cellInstanceList = oldCell.getCellInstanceList();
            assert instancePinMap.size() == cellInstanceList.size();
            Collection<EdifCellInstance> oldCellInstanceList = oldCell.getCellInstanceList();
            Instance newInstance;
            if(oldCellInstanceList != null) {
                for (EdifCellInstance edifCellInstance : oldCellInstanceList) {
                    if (cellDefinitionMap.containsKey(edifCellInstance.getCellType())) {
                        newInstance = new Instance(cellDefinitionMap.get(edifCellInstance.getCellType()));
                        newInstance.setName(edifCellInstance.getName());
                        newInstance.insertMetadata("OldName", edifCellInstance.getOldName());
                        newDefinition.addInstance(newInstance);
                    } else {
                        System.out.println("WARNING cell instanced before it is declared.");
                        System.out.println(oldCell);
                        //newInstance = new Instance(convertCell2Definition(edifCellInstance.getCellType()));
                        //cellDefinitionMap.put(edifCellInstance.getCellType(),newDefinition);
                    }
                }
            }
            return newDefinition;
        //}
    }

    private static Map<EdifPort, Port> addPortsToDefinition(EdifCell oldCell, Definition newDefinition) {
        Map<EdifPort, Port> portMap = new HashMap<>();

        Collection<EdifPort> insidePorts = oldCell.getPortList();
        for(EdifPort oldPort : insidePorts){
            Port newPort = convertEdifPort2Port(oldPort);
            newDefinition.addPort(newPort);
            portMap.put(oldPort, newPort);
        }

        return portMap;
    }

    private static Port convertEdifPort2Port(EdifPort oldPort) {
        return new Port(oldPort);
    }

    private static Definition convertLeafCell2Definition(EdifCell oldCell) {
        Definition definition = new Definition(oldCell); //get the ports out of this.
        if(!cellDefinitionMap.containsKey(oldCell)) {
            cellDefinitionMap.put(oldCell, definition);
        }
        return definition;
    }


}
