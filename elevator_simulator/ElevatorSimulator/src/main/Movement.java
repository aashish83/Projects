package main;
import java.util.ArrayList;

import model.Elevators;

public class Movement implements Runnable{

	Elevators e;
	
	public Movement(Elevators e)
	{
		this.e = e;
	}
	
	public static ArrayList<Thread> movement;
	public static void doMovement()
	{
		movement = new ArrayList<>();
		for(int e1 = 0 ; e1 < Controller.getNumberOfElevators() ; e1++)
		{
			Elevators elevator = Controller.getElevatorContainer().get(e1);
	
			Thread m = new Thread(new Movement(elevator));
			movement.add(m);
			//System.out.println("Elevator " + elevator.getId() + " is currently at floor : " + elevator.getCurrentFloor());
			m.start();
		} 
	}

	@Override
	public void run() {
		while(true)
		{ if(e==null) { } else
			try {
				e.servefloor(e);
			} catch (InterruptedException e) {
				e.printStackTrace();
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}	
		}
	}
}


