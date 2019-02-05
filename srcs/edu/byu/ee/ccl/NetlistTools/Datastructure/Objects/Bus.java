package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import edu.byu.ece.edif.core.EdifNet;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Bus extends NetlistObject {
    private List<Wire> wireList = new ArrayList<>();
    private boolean is_scalar;
    private boolean lower_index;
    private boolean is_downto;

    public Bus(EdifNet edifNet){
        super();
        wireList.add(new Wire(edifNet));
    }

    public Bus(String name){
        super();
        setName(name);
    }

    public void addWire(Wire wire){
        wireList.add(wire);
    }
}
