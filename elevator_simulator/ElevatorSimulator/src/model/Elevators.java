package model;
import java.awt.Color;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;
import java.util.PriorityQueue;
import java.util.Queue;

import javax.swing.JButton;

import main.ElevatorCalls;



public class Elevators {

    private int id;
    private double current_floor = 1;
    public static int motion_direction;
    public static final int MOVING_UP = 1;
    public static final int NO_DIRECTION = 0;
    public static final int MOVING_DOWN = -1;
    public static int door=0;
    private  int door_size = 0;
 
    private PriorityQueue<Integer> callQueue;
    
    private static int doorSize=4;

    public Elevators(int id) {
        callQueue = new PriorityQueue<Integer>();
        this.id = id;
        motion_direction = NO_DIRECTION;
        this.current_floor = 0;
    }

    public int getId() {
        return this.id;
    }


    public void setCurrentFloor(double floor) {
    
    	
        this.current_floor = floor;
    }

    public double getCurrentFloor() {
        return this.current_floor;
    }

    public PriorityQueue<Integer> getQueue() {
        return this.callQueue;
       // return this.callQueue1;
    }

  

    public void addQueue(int floor) {
        this.callQueue.add(floor);
    
        
    }
     
    
    
   

    public synchronized void servefloor(Elevators e) throws Exception {
        try {
            wait();
        } catch (InterruptedException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
try{
        while (getQueue().size() > 0) {
           // System.out.println("current floor" + getCurrentFloor() + "gotofloor" + getQueue().peek());
            if (getCurrentFloor() < getQueue().peek()) {
                double i = getCurrentFloor();
                while (i <= getQueue().peek()) { try{ if(e==null) {} }catch(Exception ax) {}
                    e.setCurrentFloor(i);
                    
                    System.out.print("\nElevator " + getId() + " is currently at floor : " + getCurrentFloor());
                    motion_direction = MOVING_UP;
                    Thread.sleep(1000);
                    i = i + 0.5; 
                }
                motion_direction = NO_DIRECTION;if (!ElevatorCalls.active_buttons.isEmpty()) { try{ if(getId()<0 &&e.getCurrentFloor()<0){ } 
                
                }catch(Exception t) {}
                	ElevatorCalls.setInternal(getId(), (int)e.getCurrentFloor(), false); }
                if(!ElevatorCalls.active_buttons1.isEmpty()) { 
               	 ElevatorCalls.setExternal((int) e.getCurrentFloor(),false); }	
                ListIterator<JButton> litr = ElevatorCalls.active_buttons1.listIterator();
              //  if((litr==litr.next())||litr.next()!=null) {System.out.println("gere"); }
                 e.open(); e.close();   		 						
                }
        
             else {
                for (double i = getCurrentFloor(); i >= getQueue().peek(); i-=0.5) { try{ if(e==null) {} }catch(Exception ax) {}
                    e.setCurrentFloor(i);
                    System.out.print("\nElevator " + getId() + " is currently at floor : " + getCurrentFloor());
                    motion_direction = MOVING_DOWN;
                    Thread.sleep(1000);
                }
                motion_direction = NO_DIRECTION;  if (!ElevatorCalls.active_buttons.isEmpty()) {  // System.out.println("Test for calling here ");
            	ElevatorCalls.setInternal(getId(), (int)e.getCurrentFloor(), false);	}																	
                
                if(ElevatorCalls.goToFloorEnteredByGui != -1) { 
               	 ElevatorCalls.setExternal((int)e.getCurrentFloor(),false);}
                ListIterator<JButton> litr = ElevatorCalls.active_buttons1.listIterator();
           
                  e.open(); e.close();
            }		
           
        	ElevatorCalls.setInternal(getId(), (int)e.getCurrentFloor(), false);																		
        	ElevatorCalls.setExternal((int)e.getCurrentFloor(),false);
        	if(getQueue().peek()==null) { 
        		try{ wait();
        		} catch(Exception a) { } }
        		else
            getQueue().remove();  
        }
          
            motion_direction = NO_DIRECTION;
      
            System.out.println();
}catch(Exception ex) {}
        }
   

    public synchronized void serveFloor2() {
        notify();
    }

    public  void open() throws Exception {   int count=0;
   
  
    	   
      for ( int doorsize = 0; doorsize < 5; doorsize++) {
    	
    	
    	  try{
    	Thread.sleep(150);
    	  setDoorSize(doorsize); 
    
    			Thread.sleep(150);
    		}catch(Exception e) { System.out.println("error is here");
        	
    		
    		
        	
               } 
      }  
    } 
    

    public void close() throws InterruptedException {
    
    	if(getDoorSize()==4)
    	  for ( int doorsize = getDoorSize(); doorsize > -1; doorsize--) {
    	    	
    	    	
    	    Thread.sleep(150);
    	    	  setDoorSize(doorsize);
    	    	Thread.sleep(150);
    	
        }
    }
    
    public int getDoorSize() {
    	
		return door_size;
	}

	public void setDoorSize(int door_size) {
		this.door_size = door_size;
	}
    
}


