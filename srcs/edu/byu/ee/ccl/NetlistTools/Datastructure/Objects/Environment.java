package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import edu.byu.ece.edif.core.*;
import edu.byu.ee.ccl.NetlistTools.Datastructure.Objects.Managers.ReferenceManager;

import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.List;

public class Environment extends NetlistObject{

    /**
     * Holds all the definitions in the environment and assigns them a unique Id that
     * can be used to reference that particular definition in the space.
     *
     * provides both the insert and lookupObject operators to allow insertion and access of definitions
     */
    private transient ReferenceManager<Definition> definitionManager = new ReferenceManager<>();
    /**
     * Holds the wires present in the design. Each wire is assigned a unique Id that can
     * reference the wire.
     *
     * provides both an insert and lookupObject operation for simple construction and access.
     */
    private transient ReferenceManager<Wire> wireManager = new ReferenceManager<>();
    /**
     * Holds all the pins in the design. Each pin is assigned a unique access Id that can
     * be used to reference the pin.
     *
     * Provides an insert and lookupObject operation for simple construction and access.
     */
    private transient ReferenceManager<Pin> pinManager = new ReferenceManager<>();

    /**
     * The list of libraries that are included in the environemnt.
     */
    List<Library> libraries = new ArrayList<>();
    /**
     * The top instance that holds all other instances in the environment
     */
    Instance topInstance;

    public int getDefinitionReference(Definition definition){
        Integer ref = definitionManager.lookupReference(definition);
        if(ref == null){
            ref = definitionManager.insert(definition);
        }
        return ref;
    }
//
//    /*
//    Functions are needed that will allow insertion of definitions, wires and pins
//     */
//
    public Environment(EdifEnvironment edifEnvironment){
        super();
        //fill up the environment based on the edif file here
        //add the date from our netlist
        if(edifEnvironment.getDate() != null){
            insertMetadata("Date", edifEnvironment.getDate().toString());
        }
        //add all string fields from our netlist
        insertMetadata("Author", edifEnvironment.getAuthor());
        insertMetadata("Program", edifEnvironment.getProgram());
        insertMetadata("OldName", edifEnvironment.getOldName());
        insertMetadata("Name", edifEnvironment.getName());
        insertMetadata("Version", edifEnvironment.getVersion());
        //add all the libraries
        //InsertLibraryList(edifEnvironment.getLibraryManager());
        //add top instance
//        InsertTopInstance(edifEnvironment.getTopCell());
    }
//
//
    public void addLibrary(Library library){
        libraries.add(library);
    }

    /**
     * Another helper function that will allow Conversion and insertion of an Edif library
     * object into the Environment. This function's purpose is to allow the easy transition
     * from the Edif tools to the newer Netlist tools
     *
     * Inserts one library using a constructor in the library class to do the conversion.
     *
     * @param edifLibrary The Edif library that will be converted into a netlist tool library
     */
    public void InsertLibrary(EdifLibrary edifLibrary){
        Library library = new Library(edifLibrary);
        libraries.add(library);
    }
//
    /**
     * This function is a helper function to create an internal representation from
     * our existing EDIF tools. Helps transfer a netlist from the edif tools to the
     * Netlist Tools
     *
     * Inserts Libraries from an existing EDIF Library manager in the EDIF tools
     * It accomplishes this task by calling the single library insert function
     * for each library in the library manager.
     *
     * @param libraryManager The Edif library manager
     */
    public void InsertLibraryList(EdifLibraryManager libraryManager){
        List<EdifLibrary> libList = libraryManager.getLibraries();
        for (EdifLibrary lib : libList ) {
            InsertLibrary(lib);
        }
    }
//
//
//    public void InsertTopInstance(EdifCell topCell){
//        Instance edifTopInstance = new Instance(topCell, this);
//        topInstance = edifTopInstance;
//    }

    /**
     * Writes out the Internal representation of the netlist to a file
     */
    public void toIR(String Filename){
        try(Writer outWriter = new FileWriter(Filename)){
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            gson.toJson(this, outWriter);
        } catch (IOException e) {
            System.out.println("invalid output file name");
            e.printStackTrace();
        }
    }
}
