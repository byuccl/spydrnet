package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifCell;
import edu.byu.ece.edif.core.EdifLibrary;
import edu.byu.ece.edif.core.PropertyList;

import java.util.*;

public class Library extends NetlistObject{

    List<Definition> definitions = new ArrayList<>();

    Library(EdifLibrary edifLibrary){
        super();
        //insertDefinitionCollection(edifLibrary.getCells());
        setName(edifLibrary.getName());
        insertMetadata("OldName", edifLibrary.getOldName());
        PropertyList propertyList = edifLibrary.getPropertyList();
        if(propertyList != null) {
            propertyList.forEach((k, v) -> insertMetadata(k, v.getValue().toString()));
        }
    }

    public void addDefinition(Definition definition){
        definitions.add(definition);
    }

    public void insertDefinitionCollection(Collection<EdifCell> edifCellList){
        edifCellList.forEach(edifCell -> insertDefinition(edifCell));
    }

    public void insertDefinition(EdifCell edifCell){
        Definition definition = new Definition(edifCell);
        definitions.add(definition);
    }
}