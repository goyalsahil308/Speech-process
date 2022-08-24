package py4j;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.*;
import java.util.ArrayList;

public class AppClass {
    Logger logger = Logger.getLogger(AppClass.class.getName());
    public String fillDataForSpeechRequest() throws IOException {
    

     /** Args   : Null
      *  Returns: String
         Takes input and return it to python
      */

        logger.setLevel(Level.INFO);
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Insufficient input\nEnter input again : ");  
        String str = br.readLine();
        logger.log(Level.INFO, "Success");
        return str;
        }

    public String enterFirstInput() throws IOException{

   /**   Args   : Null
      *  Returns: String
         Takes first input and return it to python
      */

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Enter input :");  
        String str = br.readLine();
        logger.log(Level.INFO, "Success");
        return str;        
    }
    

    public int updateNewWordsCloud(ArrayList<Object> b) { 

    /**   Args   : List of list which contains unprocessed input
      *   Returns: 0
          Updates input to cloud which couldn't be processed by python
      */

        System.out.println(b);
        logger.log(Level.INFO, "Success");
        return 0;
    }
    public int processUserActions(ArrayList<Object> c){

   /**   Args   : List of query
      *  Returns: 0
         Send query to be processed
      */

        System.out.println(c);
        logger.log(Level.INFO, "Success");
        return 0;
    }
 
     public static void main(String[] args) {

        AppClass y=new AppClass();
        GatewayServer gatewayServer = new GatewayServer(y);
        gatewayServer.start();  
        System.out.println("Gateway Server Started");
       
    }

}
