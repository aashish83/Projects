package main;

import java.util.*;

import javax.swing.JButton;

import algorithm.SchedulingAlgorithm;
import model.Elevators;
import simulator.Gui;

import java.awt.Color;
import java.math.*;

public class ElevatorCalls implements Runnable, SchedulingAlgorithm {

    public static volatile int goToFloorEnteredByGui = -1;
    public static volatile int[] goToFloorClickedByInteriorButtons;
    public static Object interiorButtonDummmy = new Object();
    public static volatile String commandType = "";
    private PriorityQueue<Integer> callQueue1;
   public static ArrayList<JButton> active_buttons1 = new ArrayList<JButton>(); 
    public static ArrayList<JButton> active_buttons = new ArrayList<JButton>(); 
    public static JButton dummy= new JButton();
    public static void listen() {
        Thread listener = new Thread(new ElevatorCalls());
        listener.start();
    }


    @Override
    public void run() {
        try {
            Scanner sc = new Scanner(System.in);
            // TODO Auto-generated method stub
            while (true) {
             
                if ("internal".equalsIgnoreCase(commandType)) {
                   
                    synchronized (interiorButtonDummmy) {active_buttons.add(Gui.internalButtonClicked);
                      
                            
                    	 if (goToFloorClickedByInteriorButtons != null) {	 
                        	
                      
                            Controller.getElevatorContainer().get(goToFloorClickedByInteriorButtons[0]).addQueue(goToFloorClickedByInteriorButtons[1]);
                            Controller.getElevatorContainer().get(goToFloorClickedByInteriorButtons[0]).serveFloor2();
                           
                   
                            
                            commandType = "";
                            
                        }
                    }
                } else if ("external".equalsIgnoreCase(commandType)) {
                    synchronized (ElevatorCalls.class) {
                        if(goToFloorEnteredByGui != -1) { 
                        	
                        	
                        	
                        	
                            Elevators chosen1 = getNearestElevator(goToFloorEnteredByGui,Elevators.motion_direction);
                          
                          // Elevators chosen1= randomElevator();
                            
                            
                            
                            chosen1.addQueue(goToFloorEnteredByGui);   active_buttons1.add(Gui.externalButtonClicked);    setExternal(goToFloorEnteredByGui,true);// System.out.println("This is callin from here External calling correctly");
                        	
                            chosen1.serveFloor2();
                           
                            commandType = "";
                        } else {
                           
                        }
                    }
                }

            }
        } catch (Exception e) {
            System.out.println("exception is in chosing the elevator" + e);
        }
    }

    @Override
    public Elevators randomElevator() {
        Random r = new Random();
        int elevator = r.nextInt(Controller.getNumberOfElevators());
        Elevators currentele = Controller.getElevatorContainer().get(elevator);
        return currentele;
    }
   
    public Elevators getNearestElevator(int floorNumber,int dir) {
        Elevators closestElevator = null;
        double closestFloor = 1;
        double max = Controller.getNumberOfFloors();


        for (int i = 0; i < Controller.getNumberOfElevators(); i++) {
            Elevators currentele = Controller.getElevatorContainer().get(i);
           
            double currentfloor = Controller.elevator_container.get(i).getCurrentFloor();
         
            

          
            if (currentfloor >= closestFloor-1 && currentfloor < floorNumber+1 ) {
                closestElevator = currentele;

                closestFloor = currentfloor;
              
  //          }
}   
   if ( currentfloor ==floorNumber) { 
                closestElevator = currentele;
            closestFloor=currentfloor;
            }
 
   else	   	if (currentfloor != floorNumber &&closestFloor!=floorNumber && Math.abs(currentfloor - floorNumber) <= max) {
                closestElevator = currentele;
                max = Math.abs(currentfloor - floorNumber);
            
            }
        
 if(currentfloor==floorNumber) {
closestElevator=currentele;
}

        }
        return closestElevator;
    }

    public int type(String ie) {
        if (ie.equals("i")) {
            return 1;
        }

        return 0;

    }
    public static void setExternal(int floor,boolean value) {
    	
    	if(value==false) {  ListIterator<JButton> k = active_buttons1.listIterator();
    	
         while(k.hasNext()) {
        	 
         	JButton b =k.next(); 
         	
         //	System.out.println(b.getName()+"froom inside the external while loop compares with" +floor);
         	if(b.getName().contains(floor+"u") || b.getName().contains(floor+"d")) {
         	b.setBackground(Color.GRAY);
         	//ElevatorCalls.goToFloorEnteredByGui =k.next();
         	dummy =b; }
         }  }
    	dummy.setBackground(Color.gray);
        active_buttons1.remove(dummy);
    	value=false;
    }
    
    public static void setInternal(int i, int j, boolean val) {
		
		 if(!val) { 
			 ListIterator<JButton> litr = active_buttons.listIterator();
	    	
			 while (litr.hasNext()) {
	            JButton b = litr.next();
	            
	          
	          
	            
	           if(b.getName().contains(i+""+(j+1))) {
	            	b.setBackground(Color.gray);
	            	dummy = b;
	            
	            }
	           
	       }
		}
		
		
		  dummy.setBackground(Color.gray);
			active_buttons.remove(dummy);
		val=false;
		
	}
  
   
}
