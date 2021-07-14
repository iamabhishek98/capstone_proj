package com.example.blecapstone;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import java.util.List;

public class MainActivity extends AppCompatActivity {
    private final static String TAG = "CAPSTONE_BLE_MAIN";
    private BluetoothLeService mBluetoothLeService;
    private String mDeviceAddress;
    private boolean mConnected;
    private NetworkThread mNet;

    // Code to manage Service lifecycle.
    private final ServiceConnection mServiceConnection = new ServiceConnection() {

        @Override
        public void onServiceConnected(ComponentName componentName, IBinder service) {
            mBluetoothLeService = ((BluetoothLeService.LocalBinder) service).getService();
            if (!mBluetoothLeService.initialize()) {
                Log.e(TAG, "Unable to initialize Bluetooth");
                finish();
            }
            // Automatically connects to the device upon successful start-up initialization.
            mBluetoothLeService.connect(3);
            mBluetoothLeService.connect(2);
            mBluetoothLeService.connect(1);
            Handler handler=new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    for(int i = 0; i<3; i++){
                        if( mBluetoothLeService.mConnectionStateList[i] == BluetoothLeService.STATE_DISCONNECTED) {
                            Log.i(TAG, "Reconnecting to Device:" +i );
                            mBluetoothLeService.connect(i+1);
                        }
                    }
                    handler.postDelayed(this,5000);
                }
            },5000);
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            mBluetoothLeService = null;
        }
    };

    // Handles various events fired by the Service.
    // ACTION_GATT_CONNECTED: connected to a GATT server.
    // ACTION_GATT_DISCONNECTED: disconnected from a GATT server.
    // ACTION_GATT_SERVICES_DISCOVERED: discovered GATT services.
    // ACTION_DATA_AVAILABLE: received data from the device.  This can be a result of read
    //                        or notification operations.
    private final BroadcastReceiver mGattUpdateReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            if (BluetoothLeService.ACTION_GATT_CONNECTED.equals(action)) {
                mConnected = true;
            } else if (BluetoothLeService.ACTION_GATT_DISCONNECTED.equals(action)) {
                mConnected = false;
            } else if (BluetoothLeService.ACTION_GATT_SERVICES_DISCOVERED.equals(action)) {
                // Show all the supported services and characteristics on the user interface.
//                printServices(mBluetoothLeService.getSupportedGattServices(deviceID));
            } else if (BluetoothLeService.ACTION_DATA_AVAILABLE.equals(action)) {
                handleBLEdata(intent.getByteArrayExtra(BluetoothLeService.EXTRA_DATA),intent.getIntExtra(BluetoothLeService.DEVICEID,0) );
            }
        }
    };


    private void printServices(List<BluetoothGattService> supportedGattServices) {
        return;
    }

    private void handleBLEdata(final byte[] data, final int ID ) {
        final StringBuilder stringBuilder = new StringBuilder(data.length);
        for(byte byteChar : data)
            stringBuilder.append(String.format("%1d ", byteChar));
        Log.i(TAG, "DEVICE: " + ID + " DATA: " + stringBuilder.toString());
//        Log.i(TAG, "datasize " +data.length );
        mNet.pushFrame(mNet.makeDataFrame(ID,data));
        return;
    }




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mDeviceAddress = BluetoothLeService.DEVICE_3_MAC;
        Log.i(TAG, "onCreate: HELLO");
        mNet = new NetworkThread();
        mNet.startnetworkTask();
        Intent gattServiceIntent = new Intent(this, BluetoothLeService.class);
        bindService(gattServiceIntent, mServiceConnection, BIND_AUTO_CREATE);

    }

    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(mGattUpdateReceiver, makeGattUpdateIntentFilter());
        if (mBluetoothLeService != null) {
            final boolean result3 = mBluetoothLeService.connect(3);
            final boolean result2 = mBluetoothLeService.connect(2);
            final boolean result1 = mBluetoothLeService.connect(1);
            Log.d(TAG, "Connect request result1=" + result1);
            Log.d(TAG, "Connect request result2=" + result2);
            Log.d(TAG, "Connect request result3=" + result3);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(mGattUpdateReceiver);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unbindService(mServiceConnection);
        mBluetoothLeService = null;
    }

    private static IntentFilter makeGattUpdateIntentFilter() {
        final IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(BluetoothLeService.ACTION_GATT_CONNECTED);
        intentFilter.addAction(BluetoothLeService.ACTION_GATT_DISCONNECTED);
        intentFilter.addAction(BluetoothLeService.ACTION_GATT_SERVICES_DISCOVERED);
        intentFilter.addAction(BluetoothLeService.ACTION_DATA_AVAILABLE);
        return intentFilter;
    }
}