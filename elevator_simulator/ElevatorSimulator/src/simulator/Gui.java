package simulator;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;

import javax.swing.*;

import main.Controller;
import main.ElevatorCalls;
import model.Elevators;



public class Gui extends JPanel {
   
   
    public static JButton externalButtonClicked;
    
    public static JButton internalButtonClicked;
    public static ArrayList<Elevators> elevator_container;
    private ElevatorCalls Calls;
    public Gui(ArrayList<Elevators> e) {
        elevator_container = e;
        this.Calls = null;
    }
    public Gui(ArrayList<Elevators> e, ElevatorCalls Calls) {
        elevator_container = e;
        this.Calls = Calls;
    }

  
  public static void createGraphics(ArrayList<Elevators> e) {


        JFrame mainframe = new JFrame("Elevator Simulator");
        mainframe.setSize(850, 650);

        Gui gui = new Gui(e);

        mainframe.setLayout(new BorderLayout());

        mainframe.add(gui, "Center");

        JPanel ebut = new JPanel();

        ebut.setLayout(new GridLayout(0, 2, 4, 12));
        extButtons(ebut);

        mainframe.add(ebut, "East");

        mainframe.setLocation(10, 50);
        mainframe.setVisible(true);
        mainframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      

        JPanel ibut = new JPanel();
        JFrame iframe = new JFrame("Interior Buttons");
        iframe.setSize(480, 370);

        ibut.setLayout(new GridLayout(e.size(), 1, 3, 25));
        intButtons(ibut);

        iframe.add(ibut);

        iframe.setLocation(870, 50);
        iframe.setVisible(true);
       iframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       
    
   
        while (true){
          
        try {
            Thread.sleep(150);
        } catch (Exception ex) {
        }
        gui.repaint();

    } }
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        int w = getSize().width; 
        int h = getSize().height;
        int p = w / 1000;
        int vert = h / 1600;
        int nfloors = Controller.getNumberOfFloors();
        int row = h / nfloors;
        int col= w / (elevator_container.size() + 1);
        g.setColor(Color.WHITE);
        int diameter = Math.min(col, row) - 2 * p;

        //levels and buttons 
        for (int k = 0; k < nfloors; ++k) {
            for (int i = 0; i < elevator_container.size(); ++i) {
                int level = row * (nfloors - k - 1);
                g.setColor(Color.green);
                g.drawLine(0, level, w, level);
                g.drawLine(0, level + 2, w, level + 2);
                g.drawLine(0, level + 4, w, level + 4);
               
            }
        }

        
        for (double i = 0; i <= nfloors - 1;i=rounding(i+0.5,1)) {
            for (int j = 0; j < elevator_container.size(); ++j) {
                int elev_level = (int) (row * (nfloors - i - 1));
              
              
                int	door = elevator_container.get(j).getDoorSize();
                if (elevator_container.get(j).getCurrentFloor() == i) {
                
					
				
                	
                	g.setColor(Color.ORANGE);
                g.fillRect(j * col + 3 * p, elev_level + p, diameter - 2 * p, diameter);
            
                	if(door>0) {
	                	g.setColor(Color.black);
	                	g.fillRect(j*col+3*p+8*(p-door) +30, elev_level+p, (int)((door/4.0)*(diameter-2*p)), diameter);
	                
					} 
                    ElevatorCalls.goToFloorEnteredByGui=-1;//  } 
                g.setColor(Color.cyan);
               
                g.drawString("" + (int) (i + 1), j * col + (p + 4) * p, elev_level + row / 3 - (p - 4));
            }
        }
            }
    }
    


    public static void extButtons(JPanel panel) {

        int num_floors = Controller.getNumberOfFloors();

        JButton[] eup = new JButton[num_floors];
        JButton[] edwn = new JButton[num_floors];

        for (int j = 0; j < num_floors; j++) {
        	final int i = j;

            eup[i] = new JButton("UP ^");
            eup[i].setActionCommand(""+(num_floors-i-1));
            eup[i].addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent e)
                {
                    synchronized (ElevatorCalls.class) {
                        ElevatorCalls.goToFloorEnteredByGui = Integer.parseInt(e.getActionCommand());
                        ElevatorCalls.commandType="external";
                        eup[i].setBackground(Color.cyan);
                        externalButtonClicked = eup[i];
                    }
                }
                
            });
            
            
            eup[i].setBackground(Color.gray);
            eup[i].setName((num_floors - 1 - i) + "u");
          

            panel.add(eup[i]);
            if (i == 0) {
                eup[i].setVisible(false);
                eup[i].setEnabled(false);
            }

            edwn[i] = new JButton("DOWN ");
        
            edwn[i].setActionCommand(""+(num_floors-i-1));
            edwn[i].addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent f)
                {
                    synchronized (ElevatorCalls.class) {
                        ElevatorCalls.goToFloorEnteredByGui = Integer.parseInt(f.getActionCommand());
                        ElevatorCalls.commandType="external";
                        edwn[i].setBackground(Color.cyan);
                        externalButtonClicked = edwn[i];
                    }
                }
            });
           
            
            edwn[i].setBackground(Color.gray);
            edwn[i].setName((num_floors - 1 - i) + "d");
         

            panel.add(edwn[i]);

            if (i == num_floors - 1) {
                edwn[i].setVisible(false);
                edwn[i].setEnabled(false);
            }

        }

    }
    public static double rounding(double value, int places) {
	    if (places < 0) throw new IllegalArgumentException();

	    BigDecimal bd = new BigDecimal(value);
	    bd = bd.setScale(places, RoundingMode.HALF_UP);
	    return bd.doubleValue();  }

    public static void intButtons(JPanel panel) {

        int nfloors = Controller.getNumberOfFloors();
        int nelevators = elevator_container.size();

        JButton[][] interior = new JButton[nelevators][nfloors];
        JLabel[] label = new JLabel[nelevators];

        for (int m = 0;  m< nelevators; m++) {
        	final int i = m;
        	
            label[i] = new JLabel("El:" + i);
            panel.add(label[i]);
            for (int n = 0; n < nfloors; n++) {
            	final int j = n;
            	
                interior[i][j] = new JButton("" + (j+1));
                interior[i][j].setActionCommand(i+":"+j);
                interior[i][j].setBackground(Color.gray);
               
                interior[i][j].addActionListener(new ActionListener()
                {
                    public void actionPerformed(ActionEvent e)
                    {
                        synchronized (ElevatorCalls.interiorButtonDummmy) {
                            ElevatorCalls.goToFloorClickedByInteriorButtons = new int[2];
                            ElevatorCalls.goToFloorClickedByInteriorButtons[0] = Integer.parseInt(e.getActionCommand().split(":")[0]);
                            ElevatorCalls.goToFloorClickedByInteriorButtons[1] = Integer.parseInt(e.getActionCommand().split(":")[1]);
                            ElevatorCalls.commandType="internal";
                            interior[i][j].setBackground(Color.cyan);
                            internalButtonClicked = interior[i][j];
                        }
                    }
                });
            
                interior[i][j].setName((i)+""+(j+1));
                panel.add(interior[i][j]);
            }
           
        }
       
    	}

   
    }


   



