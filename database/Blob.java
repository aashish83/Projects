
import java.sql.*;
import java.io.*;

public class Blob{

public static void main(String args[]){

PreparedStatement pstmt;
ResultSet rs = null;

try {
Class.forName("com.mysql.jdbc.Driver");

//Class.forName("com.mysql.jdbc.Driver");
Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/LIBRARY", "aashishm", "weginohn") ;
Statement stmt = conn.createStatement();
String filename = "001.pdf";
InputStream filecontent = new FileInputStream(filename);

String sql = "update Book set overview =(?) where isbn=0192798472";

int size = filecontent.available();
PreparedStatement ps = conn.prepareStatement(sql);
ps.setBinaryStream(1, filecontent, size);
ps.executeUpdate();

sql = "SELECT overview FROM Book";

ps  = conn.prepareStatement(sql);
rs  = ps.executeQuery();

if (rs.next()){
    InputStream contentStream = rs.getBinaryStream("overview");
    String newFilename = "new_" + filename;
    // storing the input stream in the file

    OutputStream out=new FileOutputStream(newFilename);
    byte buf[]=new byte[1024];
    int len;
    while((len=contentStream.read(buf))>0)

    out.write(buf,0,len);
    out.close();
}
conn.close();
}

catch (Exception e) {
       System.out.println("Exception is " + e);
}
}
}