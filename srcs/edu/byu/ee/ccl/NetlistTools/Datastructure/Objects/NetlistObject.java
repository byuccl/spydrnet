package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Parent class of every Netlist object. Each member and method in this object is
 * inherited by the netlist objects.
 */

public class NetlistObject {

    private String name;
    private int UID = -1;
    private Map<String, String> metadata = new HashMap<>();
    private Map<String, String> properties = new HashMap<>();
    private List<String> comments = new ArrayList<>();

    private static int currentUID = 0;

    public static int newUID(){
        int out = currentUID;
        currentUID++;
        return out;
    }

    public NetlistObject(){
        UID = NetlistObject.newUID();
    }

    /**
     * sets the name of the object
     * @param name the name to be set
     */
    public void setName(String name){
        this.name = name;
    }

    /**
     * return the name of the object
     * @return the name of the object
     */
    public String getName(){
        return name;
    }

    /**
     * Inserts a key value pair into the metadata. This will replace any existing value for the key given
     *
     * @param key the key for the metadata
     * @param value the value to be stored at the particular key
     */
    public void insertMetadata(String key, String value){
        metadata.put(key, value);
    }

    /**
     * Returns the value at the key and null if there is no value stored at that key.
     * @param key used to lookupObject in the metadata
     * @return the value stored at the key
     */
    public String getMetadata(String key){
        return metadata.get(key);
    }

    public int getUID(){
        return UID;
    }

}
