package com.example.iot_projet;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;

//for UDP

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

import static java.lang.Integer.parseInt;


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
    public Switch s;

    public static byte gto[];

    public static String write_Msg;
    public  static String ip_Num;
    public  String ip_text;
    public EditText udp_port;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // button event registration
        Button btnGetValues = (Button) findViewById(R.id.getValues);
        // textView event registration
        txtView = (TextView) findViewById(R.id.textView);

        s = (Switch) findViewById(R.id.oledPilot);


        s.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                final TextView switchBtn_txtView = (TextView) findViewById(R.id.switchBtn_txtView);


                if (isChecked) {
                    Log.d("Switch", "Switch on");
                    switchBtn_txtView.setText("Temperatur first");
                    msg = "TL";

                } else {
                    Log.d("Switch", "Switch off");
                    switchBtn_txtView.setText("Luminosity first");
                    msg = "LT";

                }

                mSendData = new SendData();


                write_Msg = msg;

                // send data
                mSendData.start();

            }
        });

        // button clicked
        btnGetValues.setOnClickListener(new View.OnClickListener() { //Envoie de la demande de données au serveur
            @Override
            public void onClick(View v) {


                Log.d("layout" , "Send data button clicked");
                // create SendData class
                mSendData = new SendData();

                msg = "getValues()";
                write_Msg = msg;

                // send data
                mSendData.start();


            }
        });




    }

    // Thread class for Data send
    class SendData extends Thread{

        TextView ip_view =  findViewById(R.id.server_ip);
        String ip_value =   ip_view.getText().toString();

        TextView udpPort_view =  findViewById(R.id.server_port);
        int port_value = Integer.valueOf(udpPort_view.getText().toString());


        public void run(){
            System.out.println("this is Thread class");
            try{
                // create UDP communication socket
                DatagramSocket socket = new DatagramSocket();
                // sever address variable

                InetAddress serverAddr = InetAddress.getByName(ip_value);


                // create send data
                byte[] buf = write_Msg.getBytes();



                // change datagram packet
                DatagramPacket packet = new DatagramPacket(buf, buf.length, serverAddr, port_value);
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
                txtView.setText("");

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