import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Scanner;

public class Admin {
	private Connection conn;
	private Statement stmt;
	private ResultSet rs;
	
	
	Scanner sc = new Scanner(System.in);
	
public Admin(){
			
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
	
public  void getBook1(){
	  
	  try{
		  System.out.println("Search a Book by 1) ISBN \n 2) title \n  3) Author \n 4)Language\n 5) Get list of all books");
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

public void insertDataBook()  // Admin to insert data into Book table
{
	
	  try {
		  String query = "INSERT INTO Book (ISBN , Title, Language, Status, Year)" + "VALUES (?,?,?,?,?);";
		  
		  PreparedStatement prepStmt = conn.prepareStatement(query);
		  
		 System.out.println("Enter the Book_ISBN");
		 String Book_Id =sc.next();
		 System.out.println("");
		String x =sc.nextLine();
		  System.out.println("Enter the Title of the Book");
		  String Title =sc.nextLine();
		  System.out.println("Enter the Language of the Book");
		  String Language =sc.nextLine();
		  System.out.println("Enter the Status of the Book");
		  String Status =sc.nextLine();
		  System.out.println("Enter the Year of the Book");
		  String Year =sc.nextLine();
		 
		 
	  prepStmt.setString(1, Book_Id);
	  prepStmt.setString(2, Title);
	  prepStmt.setString(3, Language);prepStmt.setString(4, Status);prepStmt.setString(5, Year);
	  prepStmt.addBatch();
	  prepStmt.executeUpdate();
	 prepStmt.close();
}
catch (Exception e) {
System.out.println("Inserting a book entry failed"+e);
}
}
public void insertDataMember()  // for admin to add a Member
{
	
	  try {
		  String query = "INSERT INTO Member (Member_id , Member_name,Member_type, contact_number, email,  address)" + "VALUES (?,?,?,?,?,?);";
		  
		  PreparedStatement prepStmt = conn.prepareStatement(query);
		  
		 System.out.println("Enter the Member id");
		 String Member_id =sc.next();
		 System.out.println("");
		String x =sc.nextLine();
		  System.out.println("Enter the name of the Member");
		  String Title =sc.nextLine();
		  System.out.println("Enter the type of the Member");
		  String Language =sc.nextLine();
		  System.out.println("Enter the contact number");
		  String Status =sc.nextLine();
		  System.out.println("Enter the email");
		  String Year =sc.nextLine();
		  System.out.println("Enter the address");
		  String address =sc.nextLine();
		 
	  prepStmt.setString(1, Member_id);
	  prepStmt.setString(2, Title);
	  prepStmt.setString(3, Language);prepStmt.setString(4, Status);prepStmt.setString(5, Year);prepStmt.setString(6, address);
	  prepStmt.addBatch();
	  prepStmt.executeUpdate();
	 prepStmt.close();
}
catch (Exception e) {
System.out.println("Inserting a data member failed"+e);
					}

}

public void deleteMember() 
{
	try{
	  	System.out.println("Enter the Member ID to delete");
	  	String id=sc.next();
	  	 String query3="delete from Member where Member_id = '"+id+"'" ;
	  	 PreparedStatement prepStmt1 = conn.prepareStatement(query3);
			String z =sc.nextLine();
			 prepStmt1.executeUpdate();
				System.out.println("Member is successfully deleted");
				// System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );
				
			  }
			  catch(Exception e)
			  {
				  System.out.println("Deleting a member failed" +e);
			  }
}

public void deleteBook() 
{
	try{
	  	System.out.println("Enter the Book ISBN to delete");
	  	String id=sc.next();
	  	 String query3="delete from Book where ISBN = "+id+"" ;
	  	 PreparedStatement prepStmt1 = conn.prepareStatement(query3);
			String z =sc.nextLine();
			 prepStmt1.executeUpdate();
				System.out.println("Book is successfully deleted");
				
				
			  }
			  catch(Exception e)
			  {
				  System.out.println("Deleting a book failed" +e);
			  }
}

public void getfine() 
{  try{
	  System.out.println("Search Fine by: enter 1 to search by 1)Member id \n enter 2 to search by 2)Member name \n 3) search for Members whose fine is greater than a value");
	  Integer input = sc.nextInt();
	  
	  switch(input) {
	  case 1: 
		  System.out.println("Enter Member ID to check fines");
		  String fines = sc.next() ;
		  String query2 = "SELECT m.Member_id,m.Member_name,b.fine from Member m join Borrows b where m.Member_id=b.Member_id and m.Member_id like  '%"+fines+ "%' ";   
		  
		  PreparedStatement prepStmt2 = conn.prepareStatement(query2);
			 
				String z =sc.nextLine();
		 ResultSet rs2 = prepStmt2.executeQuery(); 
		 System.out.println("Member ID" +"\t\t" + "Member Name" +"\t\t" + "FINE"  );

		  while(rs2.next()){

				System.out.println(rs2.getString("Member_id")+ "\t||" +rs2.getString("Member_name")+ "\t||" +rs2.getString("fine"));
			
		  }  break;
	  case 2: 
		  System.out.println("Enter Member Name to check for fines");
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
	 case 3: 

	 System.out.println("Enter the fine above which you want to retrieve");
	  Integer fines2 = sc.nextInt() ;
	  String query5 = "SELECT m.Member_id,m.Member_name,b.fine from Member m join Borrows b where m.Member_id=b.Member_id and b.fine > 'fines2' ";   
	 // select m.Member_id,m.Member_name,b.fine from Member m join Borrows b where m.Member_id=b.Member_id and m.Member_id like '%1%'; 
	  PreparedStatement prepStmt5 = conn.prepareStatement(query5);
		 
			String x1 =sc.nextLine();
	 ResultSet rs6 = prepStmt5.executeQuery(); 
	 System.out.println("Member ID" +"\t\t" + "Member Name" +"\t\t" + "FINE"  );

	  while(rs6.next()){

			System.out.println(rs6.getString("Member_id")+ "\t\t||" +rs6.getString("Member_name")+ "\t\t||" +rs6.getString("fine"));
		
	  }
	  
}  }  catch(Exception e) {
	  System.out.println("Searching for fines failed" +e);
}
}
public void returnBook() 
  { try {
	  System.out.println("Enter The ISBN of the Book");
	  String isbn =sc.next();
	  System.out.println("Enter The Member id");
	  String id =sc.next();
	  String query2 = "update Book set status ='available' where isbn="+ isbn +"";   
	//String query1="insert into Borrows(ISBN,Member_id,borrow_date) values ("+isbn+","+id+", NOW() ) ";
String query1="delete from Borrows where isbn="+isbn+"";
System.out.println("Your Book has been returned \n Your current Books are");
	  String query3="select Book.title,b.isbn,b.member_id,b.borrow_date,b.return_date,fine from Borrows b join Book where Book.isbn=b.isbn and b.Member_id = '+id+'" ;
	  PreparedStatement prepStmt2 = conn.prepareStatement(query2);
	  PreparedStatement prepStmt3 = conn.prepareStatement(query1);
	  PreparedStatement prepStmt1 = conn.prepareStatement(query3);
			String z =sc.nextLine();
	 prepStmt2.executeUpdate();
	 prepStmt3.executeUpdate();
	 
	 ResultSet rs2 =prepStmt1.executeQuery();
	
	// System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );
	  while(rs2.next()){

		  System.out.println(rs2.getString("title")+ "\t"+ rs2.getString("ISBN")+ "\t||" +rs2.getString("member_id")+ "\t||" +rs2.getString("borrow_date")+ "\t||" +rs2.getString("fine")+ "\t||" +rs2.getString("return_date"));
		
	  }
  }
  catch(Exception e)
  {
	  System.out.println("Book returning process failed" +e);
  }
  }

 public void checkoutBook()   // make Book status as not available if checked out. 
  { try {
	  
	  System.out.println("Enter The ISBN of the Book");
	  String isbn =sc.next();
	  System.out.println("Enter the Member id");
	  String id =sc.next();
	  String query2 = "update Book set status ='not available' where isbn="+ isbn +"";   
	 String query1="insert into Borrows(ISBN, member_id, borrow_date) values ('"+isbn+"','"+id+"', NOW() ) ";
	 String query3="select Book.title,b.ISBN,b.member_id,b.borrow_date,b.return_date,fine from Borrows b join Book where Book.isbn=b.isbn and b.member_id = '+id+'" ;
	  PreparedStatement prepStmt2 = conn.prepareStatement(query2);
	  PreparedStatement prepStmt3 = conn.prepareStatement(query1);
	  PreparedStatement prepStmt1 = conn.prepareStatement(query3);
			String z =sc.nextLine();
	 prepStmt2.executeUpdate();
	 prepStmt3.executeUpdate();
	 
	 ResultSet rs2 =prepStmt1.executeQuery();
	System.out.println("");
	// System.out.println("ISBN" +"\t\t" + "Title" +"\t\t" + "Language" +"\t\t"+"Status" +"\t\t" +"Year" +"\t\t" );
	  while(rs2.next()){

		  System.out.println(rs2.getString("title")+ "\t"+ rs2.getString("ISBN")+ "\t||" +rs2.getString("member_id")+ "\t||" +rs2.getString("borrow_date")+ "\t||" +rs2.getString("fine")+ "\t||" +rs2.getString("return_date"));
		
	  }
  } catch(Exception e)
  {
	  System.out.println("Checkingout of books failed" +e);
  }
  }
  


	public static void main(String [] args){
		
		Scanner sc = new Scanner(System.in);
		Admin connect = new Admin();
		
		System.out.print("Please choose a action  1) Insert a new Book entry  \t 2) Insert a new Member entry   \t 3) delete a Member  \n 4) Delete a Book  \t 5) Search for Books  \t   6) Show the Members who has fine \t  7) Checkout Students book \t 8) Book Returned"  );
	    Integer input =sc.nextInt();
	    
	   switch(input) {
	   
	   case 5:   connect.getBook1(); break;
	   
	   case 1: connect.insertDataBook(); break;
	  
	   
	   case 2: connect.insertDataMember();	break;
	   
	   
	   case 6: connect.getfine(); break;
	   
	
	   case 3: connect.deleteMember(); break;
	   
	   case 4: connect.deleteBook(); break;
	    
		case 7: connect.checkoutBook(); break;

		case 8: connect.returnBook(); break;
	   }
		    
	}
	

}