package algorithm;
import model.Elevators;

public interface SchedulingAlgorithm {

	public Elevators randomElevator();
	public Elevators getNearestElevator(int floorNumber,int dir);
}
