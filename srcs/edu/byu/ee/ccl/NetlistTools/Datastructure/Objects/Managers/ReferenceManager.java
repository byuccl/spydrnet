package edu.byu.ee.ccl.NetlistTools.Datastructure.Objects.Managers;

import edu.byu.ee.ccl.NetlistTools.Datastructure.Objects.Pin;

import java.util.HashMap;
import java.util.Map;

public class ReferenceManager<T> {
    private Map<Integer, T> objectMap = new HashMap<>();
    private Map<T, Integer> referenceMap = new HashMap<>();
    private int nextObject = 0;

    public int insert(T object){
        objectMap.put(nextObject,object);
        referenceMap.put(object, nextObject);
        int temp = nextObject;
        nextObject++;
        return temp;
    }

    public T lookupObject(int i){
        return objectMap.get(i);
    }

    public Integer lookupReference(T obj){
        return referenceMap.get(obj);
    }

}
