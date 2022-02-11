package com.example.mdp.tabs;

import android.app.ProgressDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.example.mdp.BluetoothConnectionService;
import com.example.mdp.R;

import java.nio.charset.Charset;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ChatFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ChatFragment extends Fragment {
    private static final String ARG_SECTION_NUMBER = "section_number";
    private static final String TAG = "Chat Fragment";

    TextView showReceived;
    EditText inputMessage;
    Button sendButton;
    public static ProgressDialog myDialog;;
    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;

    private PageViewModel pageViewModel;

    public ChatFragment() {
        // Required empty public constructor
    }

    public static ChatFragment newInstance(int index) {
        ChatFragment fragment = new ChatFragment();
        Bundle bundle = new Bundle();
        bundle.putInt(ARG_SECTION_NUMBER, index);
        fragment.setArguments(bundle);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        pageViewModel = new ViewModelProvider(this).get(PageViewModel.class);
        int index = 1;
        if (getArguments() != null) {
            index = getArguments().getInt(ARG_SECTION_NUMBER);
        }

        pageViewModel.setIndex(index);


    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        SharedPreferences sharedPreferences;

        View root =  inflater.inflate(R.layout.fragment_chat, container, false);

        showReceived = root.findViewById(R.id.showReceived);
        inputMessage = root.findViewById(R.id.inputMessage);
        sendButton = root.findViewById((R.id.sendButton));
//        trying getContext() in the getInstance
        LocalBroadcastManager.getInstance(getContext()).registerReceiver(messageReceiver, new IntentFilter("incomingMessage"));

        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                inputMessage =  root.findViewById(R.id.inputMessage);
                // write message
                String message = inputMessage.getText().toString();
                if (BluetoothConnectionService.BluetoothConnectionStatus == true) {
                    byte[] bytes = message.getBytes(Charset.defaultCharset());
                    BluetoothConnectionService.write(bytes);
                }
            }
        });

        return root;

    }

    BroadcastReceiver messageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String message = intent.getStringExtra("receivedMessage");
            Log.d(TAG,message);
            showReceived.setText(message);
        }
    };



}