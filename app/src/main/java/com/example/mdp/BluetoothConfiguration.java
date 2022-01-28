package com.example.mdp;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.Nullable;
import java.lang.*;
import java.util.Set;


public class BluetoothConfiguration extends AppCompatActivity {
    private static final int REQUEST_ENABLE_BT = 0;
    private static final int REQUEST_DISCOVER_BT = 1;

    private TextView mStatusBlueTv, mPairedTv;
    ImageView mBlueIV;
    Button mOnbtn, mOffBtn, mDiscoverbtn, mPairedBtn;
    BluetoothAdapter bluetoothAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bluetooth_setup);

        //LINK all the buttons to functions
        mStatusBlueTv = findViewById(R.id.bluetoothstatus);
        mPairedTv = findViewById((R.id.pairList));
        //mBlueIV=findViewById(R.id.blu); for icon
        mOffBtn = findViewById(R.id.offBtn);
        mOnbtn = findViewById(R.id.onBtn);
        mDiscoverbtn = findViewById(R.id.discoverableBtn);
        mPairedBtn = findViewById(R.id.getPairedBtn);

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        if (bluetoothAdapter == null) {
            mStatusBlueTv.setText("Bluetooth is off, Please on bluetooth");
        } else {
            mStatusBlueTv.setText("Bluetooth is on");
        }
//images ignore now
//        if(bluetoothAdapter.isEnabled()){
//            mBlueIV.setImageResource();
//        }
//        else{
//            mBlueIV.setImageResource();
//        }
        mOnbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!bluetoothAdapter.isEnabled()){
                    showToast("Turning on bluetooth");
                    Intent intent=new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                    startActivityIfNeeded(intent,REQUEST_ENABLE_BT);
                }else{
                    showToast("bluetooth is already on");
                }
            }
        });
        mDiscoverbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!bluetoothAdapter.isDiscovering()){
                    showToast("Making Your Device Visible");
                    Intent intent=new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
                    startActivityIfNeeded(intent,REQUEST_DISCOVER_BT);
                }
            }
        });

        mOffBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(bluetoothAdapter.isEnabled()){
                    bluetoothAdapter.disable();
                    showToast("Turning off Bluetooth");
                    //add new function to off bluetooth
                }else{
                    showToast("Bluetooth is already off");
                }
            }
        });

        mPairedBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (bluetoothAdapter.isEnabled()) {
                    mPairedTv.setText("Paired Devices");
                    Set<BluetoothDevice> devices = bluetoothAdapter.getBondedDevices();

                    for (BluetoothDevice device : devices) {
                        mPairedTv.append("\n Device : " + device.getName() + " , " + device);
                    }
                } else {
                    showToast("Turn On bluetooth to get paired devices");
                }
            }
        });
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {

        switch (requestCode) {
            case REQUEST_ENABLE_BT:
                if (resultCode == RESULT_OK) {
                    showToast("Bluetooth is On");
                } else {
                    showToast("Bluetooth is Off");
                }
                break;
        }
        super.onActivityResult(requestCode, resultCode, data);

    }

    private void showToast(String msg) {
        Toast.makeText(getApplicationContext(), msg, Toast.LENGTH_SHORT).show();
    }

}
