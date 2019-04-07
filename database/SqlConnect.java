


import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.util.*;
public class SqlConnect {

	private Connection conn;
	private Statement stmt;
	private ResultSet rs;
	
	
	Scanner sc = new Scanner(System.in);
	
public SqlConnect(){
			
	try{
		Class.forName("com.mysql.jdbc.Driver");
		 conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/LIBRARY", "aashishm", "weginohn");
		 stmt = conn.createStatement();
		System.out.println("connection successful");
		
	}
  catch (Exception e) {
	  				System.out.println("exception"+ e);
  					}
			}
  public void getBook(){
	  
  try{
	  System.out.println("Search a Book by 1) ISBN \n 2) title \n  3) Author \n 4)Language  \n 5) Get list of all books");
	  Integer input=sc.nextInt();
	  

	  switch(input)
	  {
	   case 1:
			  System.out.println("enter the ISBN to search");
			  String ISBN =sc.next();                      
			  String query = "select * from Book where isbn like '%"+ISBN+"%' ";  // sql query
			 
				 PreparedStatement prepStmt = conn.prepareStatement(query);
				// prepStmt.setLong(1,ISBN);
		
				System.out.println("");
					String x =sc.nextLine();
			
				ResultSet rs= prepStmt.executeQuery();
				System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );

			  while(rs.next()){
					
					System.out.println(rs.getString("ISBN")+ "\t||" +rs.getString("Title")+ "\t||" +rs.getString("language")+ "\t||" +rs.getString("status")+ "\t||" +rs.getString("year"));
					System.out.println("");
			 
				 }
			  break;
		  
		
		  case 2:   // by_title
			
		  System.out.println("enter the title to search");// enter title
		  String Title = sc.next() ;
		  String query1 = "SELECT * FROM Book where title like '%"+Title+ "%'";  
		PreparedStatement prepStmt1 = conn.prepareStatement(query1);
		 
			String q =sc.nextLine();
	 ResultSet rs1 = prepStmt1.executeQuery(); 
	 System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );

	  while(rs1.next()){

			System.out.println(rs1.getString("ISBN")+ "\t||" +rs1.getString("Title")+ "\t||" +rs1.getString("language")+ "\t||" +rs1.getString("status")+ "\t||" +rs1.getString("year"));
		
	  					}
		
		  		break;
		  
		  
	  case 3:   // by_Author
			
		  System.out.println("enter the Author name to search");// enter title
		  String Author = sc.next() ;
	  String query2 = "SELECT *,a.Author_name FROM Book b join Writes w join Author a where a.Author_id=w.Author_id and b.isbn=w.isbn and a.Author_name like '%"+Author+ "%'";   

	  PreparedStatement prepStmt2 = conn.prepareStatement(query2);
		 
			String z =sc.nextLine();
	 ResultSet rs2 = prepStmt2.executeQuery(); 
	 System.out.println("Author Name"+"\t\t" + "ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );

	  while(rs2.next()){

			System.out.println(rs2.getString("Author_name")+"\t||"+ rs2.getString("ISBN")+ "\t||" +rs2.getString("Title")+ "\t||" +rs2.getString("language")+ "\t||" +rs2.getString("status")+ "\t||" +rs2.getString("year"));
		
	  					}
		 break;
	
  case 4: 
	  System.out.println("enter the language to search");
	 String language =sc.next();                      
	  String query12 = "select * from Book where language= ?";  // sql query
	 
		 PreparedStatement prepStmt12 = conn.prepareStatement(query12);
		 prepStmt12.setString(1,language);

		System.out.println("");
			String x1 =sc.nextLine();
	
		ResultSet rs22= prepStmt12.executeQuery();
		System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );

	  while(rs22.next()){
			
			System.out.println(rs22.getString("ISBN")+ "\t||" +rs22.getString("Title")+ "\t||" +rs22.getString("language")+ "\t||" +rs22.getString("status")+ "\t||" +rs22.getString("year"));
			System.out.println("");
	 
		 }
	  break;
case 5:
 String query5 = "select * from Book ";  // sql query
			 
				 PreparedStatement prepStmt7 = conn.prepareStatement(query5);
				// prepStmt.setLong(1,ISBN);
		
				System.out.println("");
					String x5 =sc.nextLine();
			
				ResultSet rs8= prepStmt7.executeQuery();
				System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );

			  while(rs8.next()){
					
					System.out.println(rs8.getString("ISBN")+ "\t||" +rs8.getString("Title")+ "\t||" +rs8.getString("language")+ "\t||" +rs8.getString("status")+ "\t||" +rs8.getString("year"));
					System.out.println("");
			 
				 }
			  break;

	 
	  }
  }catch(Exception ex) {
	  System.out.println( "Book Search failed"+ ex);
	  					}
  }
  public void getfine() 
  {  try{
	  System.out.println("Search Fine by: enter 1 to search by 1)Member id \n enter 2 to search by 2)Member name");
	  Integer input = sc.nextInt();
	  
	  switch(input) {
	  case 1: 
		  System.out.println("Enter Member ID to view fines");
		  String fines = sc.next() ;
		  String query2 = "SELECT m.Member_id,m.Member_name,b.fine from Member m join Borrows b where m.Member_id=b.Member_id and m.Member_id like  '%"+fines+ "%' ";   
		  
		  PreparedStatement prepStmt2 = conn.prepareStatement(query2);
			 
				String z =sc.nextLine();
		 ResultSet rs2 = prepStmt2.executeQuery(); 
		 System.out.println("Member ID" +"\t\t" + "Member Name" +"\t\t" + "FINE"  );

		  while(rs2.next()){

				System.out.println(rs2.getString("Member_id")+ "\t||" +rs2.getString("Member_name")+ "\t||" +rs2.getString("fine"));
			
		  } break;
	  case 2: 
		  System.out.println("Enter Member Name to view fines");
		  String fines1 = sc.next() ;
		  String query1 = "SELECT m.Member_id,m.Member_name,b.fine from Member m join Borrows b where m.Member_id=b.Member_id and m.Member_name like  '%"+fines1+ "%' ";   
		 // select m.Member_id,m.Member_name,b.fine from Member m join Borrows b where m.Member_id=b.Member_id and m.Member_id like '%1%'; 
		  PreparedStatement prepStmt1 = conn.prepareStatement(query1);
			 
				String x =sc.nextLine();
		 ResultSet rs1 = prepStmt1.executeQuery(); 
		 System.out.println("Member ID" +"\t\t" + "Member Name" +"\t\t" + "FINE"  );

		  while(rs1.next()){

				System.out.println(rs1.getString("Member_id")+ "\t||" +rs1.getString("Member_name")+ "\t||" +rs1.getString("fine"));
			
		  }
		  
	  }  }  catch(Exception e) {
			  System.out.println("Retrieving fines failed" +e);
		  }
	  }
  
  
  public void getList()
  { try{
  	System.out.println("Enter your Member id");
  	String id=sc.next();
  	 String query3="select Book.title,b.isbn,b.member_id,b.borrow_date,b.return_date,fine from Borrows b join Book where Book.isbn=b.isbn and b.Member_id = '"+id+"'" ;
  	 PreparedStatement prepStmt1 = conn.prepareStatement(query3);
		String z =sc.nextLine();
		 ResultSet rs2 =prepStmt1.executeQuery();
			System.out.println("Your Books are");
			 System.out.println("Member ID" +"\t\t" + "Title" +"\t\t" + "ISBN" +"\t\t"+"Borrow Date" +"\t\t" +"Fine" +"\t\t" + "Return Date" );
			  while(rs2.next()){

				  System.out.println( rs2.getString("Member_id")+"\t\t||"+rs2.getString("title")+ "\t||"+ rs2.getString("ISBN")+ "\t\t||" +rs2.getString("borrow_date")+ "\t\t||" +rs2.getString("fine")+ "\t\t||" +rs2.getString("return_date"));
				
			  }
		  }
		  catch(Exception e)
		  {
			  System.out.println("Getting your book list failed" +e);
		  }
		  }
  
  
  



public static void main(String [] args){
	
	Scanner sc = new Scanner(System.in);
	SqlConnect connect = new SqlConnect();
	
	System.out.print("Please choose a action 1) Search Books  \t     2) getfine \t   3) your Books "  );
    Integer input =sc.nextInt();
    
   switch(input) {
   
   case 1: connect.getBook(); break;
   
   

   case 2: connect.getfine(); break;
   
  
   
   case 3:connect.getList(); break;
   
  
  
   }
	    
}
}
