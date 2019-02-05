package edu.byu.ee.ccl;

import edu.byu.ece.edif.arch.ClockingArchitecture;
import edu.byu.ece.edif.arch.xilinx.XilinxClockingArchitecture;
import edu.byu.ece.edif.core.EdifCellInstance;
import edu.byu.ece.edif.core.EdifEnvironment;
import edu.byu.ece.edif.core.EdifPrintWriter;
import edu.byu.ece.edif.util.parse.EdifParser;
import edu.byu.ece.edif.util.parse.ParseException;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class CCNetsOverHierarchy {

    //object that represents the netlist in java
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

    public void writeNetlistFile(String filename) {
        EdifPrintWriter epw = null;
        try {
            epw = new EdifPrintWriter(new FileOutputStream(filename));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        netlist.toEdif(epw);
        epw.close();
    }

    //iterate each flipflop in the design
    private void iterateFlops(EdifCellInstance top){
        System.out.println(top);
        //if the level is a terminal node or a leaf:
        ClockingArchitecture clkArch = new XilinxClockingArchitecture();
        if(clkArch.isSequential(top.getCellType())) {
            System.out.println("\tSequential cell");

            if(onNewClock(top)) {
                markCell(top);
            }
        }
        //otherwise
        else {
            //System.out.println("\tnot leaf cell");
            Iterator<EdifCellInstance> children = top.getCellType().cellInstanceIterator();
            //for each of the sub nodes
            while (children.hasNext()) {
                //call this function
                iterateFlops(children.next());
            }
        }
    }

    private class Clock{
        private String name;
        Clock(String domain){
            name = domain;
        }

        @Override
        public boolean equals(Object obj) {
            if(obj == null){
                return false;
            }
            if(obj.getClass() != this.getClass()){
                return false;
            }
            Clock cobj = (Clock) obj;
            return name.equals(cobj.name);
        }
    }

    //see if that FF is on a new clock domain from the feeder FF
    public boolean onNewClock(EdifCellInstance ecell){
        Clock mclock = getDrivingClock(ecell);
        Set<EdifCellInstance> fflops = getFeederFlops(ecell);
        //run this for loop just on all the flip flops to see if one is a different cell
        for (EdifCellInstance ff : fflops) {
            if(!clocksMatch(mclock, getDrivingClock(ff))){
                return true;
            }
        }
        return false;
    }

    //get the clock domain of the FF
    private Clock getDrivingClock(EdifCellInstance ecell){
        /*TODO: get the clock domain of ecell*/
        String domain = "";
        return new Clock(domain);
    }

    //gets a list of all the FF that feed the FF in question
    private Set<EdifCellInstance>  getFeederFlops(EdifCellInstance ecell){
        Set<EdifCellInstance> feeders = new HashSet<EdifCellInstance>();
        //TODO: populate feeders with the feeder flip flops that feed the cell in question
        return feeders;
    }

    //takes the clock passed in and the feeder flops and sees if they are the same
    private boolean clocksMatch(Clock c1, Clock c2){
        //TODO: make sure the clocks match and return it.
        return false;
    }

    private void markCell(EdifCellInstance ecell){
        //TODO: mark the cell as a synchronizer.

    }

    public static void main(String[] args){
        System.out.println("Reading EDIF file");
        Edif2graph edif2graph = new Edif2graph();
        edif2graph.readNetlistFile(
                "C:\\Users\\ecestudent\\Desktop\\temp.edf"
        );//args[0]);
        edif2graph.generateGraph(
                "C:\\Users\\ecestudent\\Desktop\\edges.txt",
                "C:\\Users\\ecestudent\\Desktop\\nodes.txt"
        );
        edif2graph.writeNetlistFile(
                "C:\\Users\\ecestudent\\Desktop\\out.edif"
        );//args[1]);
    }
}