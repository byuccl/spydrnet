package edu.byu.ee.ccl;


import edu.byu.ece.edif.core.*;
import edu.byu.ece.edif.util.parse.EdifParser;
import edu.byu.ece.edif.util.parse.ParseException;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.*;

/**
 * Class that can be used to read in EDIF Files and output them to a graph file representation.
 * The graph file output format will be a numbered list of all nodes for the graph and a list
 * of edges of the format (node1, node2)
 */
public class Edif2graph {
    //object that represents the netlist in java
    private EdifEnvironment netlist;

    private Map<EdifCellInstance, Integer> cellNumberMap = new HashMap<EdifCellInstance, Integer>();
    private int nextCellNumber = 0; //-1 should not be used. it is used for no number

    private Set<connection> connectionSet = new HashSet<connection>();

    /**
     * Reads in an EDIF file.
     * @param filename the name of the file that will be read in. Must be in EDIF format.
     */
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


    private EdifPrintWriter nodeWriter;
    private EdifPrintWriter edgeWriter;

    public void generateGraph(String edges, String nodes) {

        //open a writer for the node file and the edge file.
        EdifPrintWriter nodeWriter = null;
        try {
            nodeWriter = new EdifPrintWriter(new FileOutputStream(nodes));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        EdifPrintWriter edgeWriter = null;
        try {
            edgeWriter = new EdifPrintWriter(new FileOutputStream(edges));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        //get top node
        EdifCellInstance topCell = netlist.getTopCellInstance();
        //call my recursive grapher function for the top node
        recurse_structure(topCell);

        //close the writers
        nodeWriter.close();
        edgeWriter.close();

    }

    private void recurse_structure(EdifCellInstance top){
        System.out.println(top);
        //if the level is a terminal node or a leaf:
        if(top.getCellType().isLeafCell()) {
            System.out.println("\tleaf cell");
            //assign a number
            int cellNum = assignNumber(top);
            System.out.println("\tassigned number " + cellNum);
            //find and report all connections (out direction) assigning numbers where needed...
            findOutgoingConnections(top, cellNum);
        }
        //otherwise
        else {
            //System.out.println("\tnot leaf cell");
            Iterator<EdifCellInstance> children = top.getCellType().cellInstanceIterator();
            //for each of the sub nodes
            while (children.hasNext()) {
                //call this function
                recurse_structure(children.next());
            }
        }
    }


    private void findOutgoingConnections(EdifCellInstance ecell, int cellNum){
        /*System.out.println("TODO: add various cases where the leafs are at different locations for this function");
        //for each out port of the cell
        System.out.println(ecell.getOuterNets());
        Map<EdifSingleBitPort, EdifNet> outerNets = ecell.getOuterNets();
        //this function could be really helpful
        //new EdifNet().getSinkPortRefs(boolean tristate, boolean includeTopPorts)
        for(Map.Entry<EdifSingleBitPort, EdifNet> entry : outerNets.entrySet()) {
            //follow to the connected cell
            EdifNet currentNet = entry.getValue();
            Collection<EdifPortRef> endPort = currentNet.getSinkPortRefs(false,false);
            //iterate through the end points too.
            for(EdifPortRef ref : endPort) {
                EdifCellInstance portCell = ref.getCellInstance();

                System.out.println("\tendpoint: " + ref.getCellInstance());
                //assign the cell a number
                int endPoint = assignNumber(ref.getCellInstance());
                //if the connection has not been made add it to the list of connections
                addConnection(cellNum, endPoint);
            }

        }*/
        ConnectedLeafCells clc = new ConnectedLeafCells();
        clc.addLeafCellsRecurse(null, ecell);
        List<EdifCellInstance> ecl = clc.getLeafList();
        for(EdifCellInstance e : ecl){
            int endPoint = assignNumber(e);
            addConnection(cellNum, endPoint);
        }
        //System.out.println();
    }



    private class ConnectedLeafCells{
        private List<EdifCellInstance> leaf;
        private Set<EdifCellInstance> alreadyChecked;

        ConnectedLeafCells(){
            leaf = new ArrayList<>();
            alreadyChecked = new HashSet<>();
        }

        public void reset(){
            leaf = new ArrayList<>();
            alreadyChecked = new HashSet<>();
        }

        public void addLeafCellsRecurse(EdifCellInstance last, EdifCellInstance next){
            if(alreadyChecked.contains(next)){
                return;
            }
            else{
                alreadyChecked.add(next);
            }
            //System.out.println("adding leaf cells");
            if(next.getCellType().isLeafCell() && last != null){
                //System.out.println("is leaf");
                addCell(next);
            }
            else{
                //System.out.println("not leaf following connections");
                Map<EdifSingleBitPort, EdifNet> outerNets = next.getOuterNets();

                //this function could be really helpful
                //new EdifNet().getSinkPortRefs(boolean tristate, boolean includeTopPorts)
                for(Map.Entry<EdifSingleBitPort, EdifNet> entry : outerNets.entrySet()) {
                    //follow to the connected cell
                    EdifNet currentNet = entry.getValue();
                    Collection<EdifPortRef> endPort = currentNet.getSinkPortRefs(false,true);
                    //iterate through the end points too.
                    for(EdifPortRef ref : endPort) {
                        EdifCellInstance portCell = ref.getCellInstance();

                        if(portCell == null){
                            break;
                        }

                        //System.out.println("\tendpoint: " + ref.getCellInstance());
                        //assign the cell a number
                        //int endPoint = assignNumber(ref.getCellInstance());
                        if (!alreadyChecked.contains(portCell)){//!portCell.equals(last) && !portCell.equals(next)){
                            addLeafCellsRecurse(next, portCell);
                            alreadyChecked.add(portCell);
                        }
                    }
                }
            }
        }

        public List<EdifCellInstance> getLeafList(){
            return leaf;
        }

        private void addCell(EdifCellInstance ecell){
            leaf.add(ecell);
        }

    }

    private class connection{
        private int start;
        private int end;

        public connection(int s, int e){
            start = s;
            end = e;
        }

        @Override
        public int hashCode() {
            return end*1000 + end + start;
        }

        @Override
        public String toString(){
            return "(" + start + ", " + end + ")";
        }
    }

    private void addConnection(int start, int end){
        //get rid of single element loops.
        if (start == end){
            return;
        }
        connection c = new connection(start, end);
        //add the connection to our set
        boolean added = connectionSet.add(c);
        //if the connection was added successfully
        if(added){
            //go ahead and write the connection out to the file.
            //System.out.print(c + " ");
            //WriteConnection(c);
        }
    }

    private int assignNumber(EdifCellInstance ecell){
        if (!ecell.getCellType().isLeafCell()){
            System.out.println("WARNING ASSIGNING NUMBER TO NON LEAF NODE");
        }
        //if the cell doesn't hava a number
        int cellNum = getCellNumber(ecell);
        if(cellNum == -1){
            //assign the cell the next number available
            cellNumberMap.put(ecell, nextCellNumber);
            int myCellNum = nextCellNumber;
            nextCellNumber++;
            //return the assigned number
            return myCellNum;
        }
        //otherwise return the number
        return cellNum;
    }


    private int getCellNumber(EdifCellInstance ecell){
        Integer currentNum = cellNumberMap.get(ecell);
        if(currentNum == null) {
            return -1;
        }
        return currentNum;
    }




    //reads in the edif then outputs it as a graph
    public static void main(String[] args) {
        System.out.println("Reading EDIF file");
        Edif2graph edif2graph = new Edif2graph();
        edif2graph.readNetlistFile("C:\\Users\\ecestudent\\Desktop\\temp.edf");//args[0]);
        edif2graph.generateGraph("C:\\Users\\ecestudent\\Desktop\\edges.txt","C:\\Users\\ecestudent\\Desktop\\nodes.txt");
        edif2graph.writeNetlistFile("C:\\Users\\ecestudent\\Desktop\\out.edif");//args[1]);
        System.out.println(edif2graph.netlist.toString());
    }
}
