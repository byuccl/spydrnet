package edu.byu.ee.ccl.NetlistTools.Datastructure;

import edu.byu.ece.edif.core.EdifEnvironment;
import edu.byu.ece.edif.util.parse.EdifParser;
import edu.byu.ece.edif.util.parse.ParseException;
import edu.byu.ee.ccl.NetlistTools.Datastructure.Objects.Environment;
import edu.byu.ee.ccl.NetlistTools.Datastructure.Objects.Traverse;

import java.io.FileNotFoundException;

public class FillStructure {
    //Edif netlist in java
    private EdifEnvironment netlist;

    public void readNetlistFile(String filename) {
        try {
            netlist = EdifParser.translate(filename);
        } catch (ParseException e) {
            System.out.println("[ERROR] Failed to parse EDIF.");
            e.printStackTrace();
            System.exit(-1);
        } catch (FileNotFoundException e) {
            System.out.println("[ERROR] File " + filename + " not found.");
            e.printStackTrace();
        }
    }

    public void fill(){
        //create a new environment based on the netlist
        //Environment fromEdif = new Environment(netlist);
        Traverse.Main(null);
        //this will output the system to the intermediate representation.
        Environment fromEdif = Traverse.EnvironmentOut;
        fromEdif.toIR("C:\\Users\\ecestudent\\Desktop\\out.json");
    }

    public static void main(String[] args){

        FillStructure fillStructure = new FillStructure();
        fillStructure.readNetlistFile("C:\\Users\\ecestudent\\Desktop\\temp.edf");
        fillStructure.fill();
    }
}
