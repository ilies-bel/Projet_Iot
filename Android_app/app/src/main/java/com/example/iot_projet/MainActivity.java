package com.example.iot_projet;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

//for UDP
import com.example.iot_projet.R;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;


public class MainActivity extends AppCompatActivity {

    //public static final String sIP = "10.0.0.26";   // RaspBerry Pi ip address
    //public static final String sIP = "10.0.0.21";   // Orange Pi ip address
    //public static final String sIP = "10.0.0.26";   // Nano Pi ip address
    //public static final String sIP = "10.0.0.46";   // Orange Pi ip address
    //public static final String sIP = "10.0.0.32";   // Nano Pi ip address
    //public static final String sIP = "223.62.219.58";   // S9+ Pi ip address
    public static final String sIP = "192.168.0.20";   // Nano Pi ip address
    public static final int sPORT = 10000;           // Port
    public static String ip_address;

    private String msg;
    private String return_msg;

    // Send data class
    public SendData mSendData = null;
    // display TextView
    public TextView txtView = null;

    public EditText sendMsg;

    /*ip address info*/
    public EditText ip_Num;
    public TextView ip_text;

    public static byte gto[];

    public static String write_Msg;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // button event registration
        Button btnGetValues = (Button) findViewById(R.id.getValues);
        // textView event registration
        txtView = (TextView) findViewById(R.id.textView);

        ip_Num = (EditText) findViewById(R.id.send_ip);

        // button clicked
        btnGetValues.setOnClickListener(new View.OnClickListener() { //Envoie de la demande de données au serveur
            @Override
            public void onClick(View v) {

                Log.d("layout" , "Send data button clicked");
                // create SendData class
                mSendData = new SendData();
                // send data
                mSendData.start();

                msg = "getValues()";

                write_Msg = msg.toString();
            }
        });




    }

    // Thread class for Data send
    class SendData extends Thread{
        public void run(){
            System.out.println("this is Thread class");
            try{
                // create UDP communication socket
                DatagramSocket socket = new DatagramSocket();
                // sever address variable
                InetAddress serverAddr = InetAddress.getByName(sIP);

                Log.d("UDP", String.valueOf(serverAddr));

                // create send data
                byte[] buf = write_Msg.getBytes();

                Log.d("UDP", String.valueOf(buf));

                // change datagram packet
                DatagramPacket packet = new DatagramPacket(buf, buf.length, serverAddr, sPORT);
                Log.d("UDP", "send packet.... " + "< " + new String(buf) + " >");

                //System.out.print("Send data -> ");
                byte_to_ascii(buf);
                //System.out.println();

                // send packet
                socket.send(packet);
                Log.d("UDP", "send....");
                Log.d("UDP", "Done.");

                // wait receive data
                socket.receive(packet);
                Log.d("UDP", "Receive : " + new String(packet.getData()));

                // if receive data -> String change
                String msg = new String(packet.getData());

                // view textView
                txtView.setText(msg);


            }catch (Exception e){
                Log.d("UDP", "Client: Error", e);
            }
        }
    }

    public static void byte_to_ascii(byte[] b){
        System.out.println("Ascii format : ");
        for (int i=0; i<b.length; i++){
            System.out.print((int)b[i] + " ");
        }
        System.out.println();
    }
}