package com.example.test_iot_project;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.EditText;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;


import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private Button btn1;
    private TextView textView1;
    private TextView textView2;
    @SuppressLint("UseSwitchCompatOrMaterialCode")
    private Switch switch1;
    private EditText ipserv;
    private EditText port;
    private String ip;
    private String ipport;
    private DatagramPacket packet;
    private DatagramSocket socket;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btn1 = (Button)findViewById(R.id.btn1);
        textView1 = (TextView)findViewById(R.id.textView1);
        textView2 = (TextView)findViewById(R.id.textView2);
        switch1 = (Switch)findViewById(R.id.switch1);
        ipserv = (EditText)findViewById(R.id.ipserv);
        port = (EditText)findViewById(R.id.port);

        btn1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*Initialiser la com */
                /*ip = ipserv.getText().toString();*/
                /*ipport = port.getText().toString();*/
                if (switch1.isChecked()) {
                    textView1.setText("Lumière");
                    textView2.setText("Température");
                }
                else {
                    textView1.setText("Température");
                    textView2.setText("Lumière");
                }
            }
        });

    }

    public void run() {

    }
}