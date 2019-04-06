package main;
import java.util.ArrayList;
import java.util.Scanner;

import model.Elevators;
import simulator.Gui;



public class Controller {
	public static ArrayList<Elevators> elevator_container;
	private static int num_floors;
	private static int num_elevators;
	public static void main(String[] args){ 
		
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter number of floors : ");
		num_floors = sc.nextInt(); 
        System.out.println(); //adds a new line

		System.out.print("Enter number of elevators: ");
		num_elevators = sc.nextInt();
        System.out.println();   //adds a new line
	try{ if(num_floors<1||num_elevators<1 ){
		System.out.println("enter valid values of number floor and elevators ");
	} else{
		elevator_container = new ArrayList<>();
		//Make elevators
		for(int e = 0 ; e < Controller.getNumberOfElevators() ; e++)
		{
			Elevators elevator = new Elevators(e);
			elevator_container.add(elevator);
		}

		Movement.doMovement();
		ElevatorCalls.listen();
		new Gui(elevator_container);
		Gui.createGraphics(elevator_container);
	}} catch(Exception e) {System.out.println("enter a valid number of elevator and floor"); }
	}
	public static int getNumberOfFloors()
	{
		return num_floors;
	}
	
	public static int getNumberOfElevators( )
	{
		return num_elevators;
	}
	
	public static ArrayList<Elevators> getElevatorContainer()
	{
		return elevator_container;
	}

}
