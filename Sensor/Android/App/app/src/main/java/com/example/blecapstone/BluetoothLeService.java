/*
 * Copyright (C) 2013 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.blecapstone;

import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Service for managing connection and data communication with a GATT server hosted on a
 * given Bluetooth LE device.
 */
public class BluetoothLeService extends Service {
    private final static String TAG = "CAPSTONE_BLE_SERVICE";

    public static final String DEVICE_1_MAC = "80:30:DC:D9:0C:D2";
    public static final String DEVICE_2_MAC = "80:30:DC:D9:0C:A1";
    public static final String DEVICE_3_MAC = "80:30:DC:D9:1C:3F";



    public static final String SERIAL_PORT_UUID = "0000dfb1-0000-1000-8000-00805f9b34fb";

    private BluetoothManager mBluetoothManager;
    private BluetoothAdapter mBluetoothAdapter;
    private String mBluetoothDeviceAddress_Device1;
    private String mBluetoothDeviceAddress_Device2;
    private String mBluetoothDeviceAddress_Device3;
//    private BluetoothGatt mBluetoothGatt;
    public BluetoothGatt mBluetoothGattList[] = {null,null,null};
    public int mConnectionStateList[] = {STATE_DISCONNECTED,STATE_DISCONNECTED,STATE_DISCONNECTED};



    public static final int STATE_DISCONNECTED = 0;
    public static final int STATE_CONNECTING = 1;
    public static final int STATE_CONNECTED = 2;

    public final static String ACTION_GATT_CONNECTED =
            "com.example.bluetooth.le.ACTION_GATT_CONNECTED";
    public final static String ACTION_GATT_DISCONNECTED =
            "com.example.bluetooth.le.ACTION_GATT_DISCONNECTED";
    public final static String ACTION_GATT_SERVICES_DISCOVERED =
            "com.example.bluetooth.le.ACTION_GATT_SERVICES_DISCOVERED";
    public final static String ACTION_DATA_AVAILABLE =
            "com.example.bluetooth.le.ACTION_DATA_AVAILABLE";
    public final static String EXTRA_DATA =
            "com.example.bluetooth.le.EXTRA_DATA";
    public final static String DEVICEID =
            "com.example.bluetooth.le.DEVICEID";


    // Implements callback methods for GATT events that the app cares about.  For example,
    // connection change and services discovered.
    private final BluetoothGattCallback mGattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            String intentAction;
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                intentAction = ACTION_GATT_CONNECTED;
                updateConnectionState(STATE_CONNECTED,getDeviceId(gatt)) ;
                broadcastUpdate(intentAction);
                Log.i(TAG, "Connected to GATT server.");
                // Attempts to discover services after successful connection.
                Log.i(TAG, "Attempting to start service discovery:" +
                        gatt.discoverServices());

            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                intentAction = ACTION_GATT_DISCONNECTED;
                updateConnectionState(STATE_DISCONNECTED,getDeviceId(gatt)) ;
                Log.i(TAG, "Disconnected from GATT server.");
                broadcastUpdate(intentAction);
            }
        }

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            int deviceID = getDeviceId(gatt);
            if (status == BluetoothGatt.GATT_SUCCESS) {
                broadcastUpdate(ACTION_GATT_SERVICES_DISCOVERED);
                BluetoothGattCharacteristic mSerialChar = extact_serialCharacteristic(getSupportedGattServices(deviceID));
                if (mSerialChar != null){
                    setCharacteristicNotification(mSerialChar, true, deviceID);
                }
            } else {
                Log.w(TAG, "onServicesDiscovered received: " + status);
            }
        }

        @Override
        public void onCharacteristicRead(BluetoothGatt gatt,
                                         BluetoothGattCharacteristic characteristic,
                                         int status) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                broadcastUpdate(ACTION_DATA_AVAILABLE, characteristic,gatt.getDevice().getAddress());
            }
        }

        @Override
        public void onCharacteristicChanged(BluetoothGatt gatt,
                                            BluetoothGattCharacteristic characteristic) {

            broadcastUpdate(ACTION_DATA_AVAILABLE, characteristic, gatt.getDevice().getAddress());
        }
    };

    private void broadcastUpdate(final String action) {
        final Intent intent = new Intent(action);
        sendBroadcast(intent);
    }

    private void updateConnectionState(final int state, final int ID){
        mConnectionStateList[ID-1] = state;
    }
    public String getDeviceMac(final int UUID){
        String devID = null;
        switch (UUID) {
            case 1:
                devID = DEVICE_1_MAC;
                break;
            case 2:
                devID = DEVICE_2_MAC;
                break;
            case 3:
                devID = DEVICE_3_MAC;
                break;
        }
        return devID;
    }
    public int getDeviceId(BluetoothGatt gatt){
        final String UUID = gatt.getDevice().getAddress();
        int devID = 0;
        switch (UUID) {
            case DEVICE_1_MAC:
                devID = 1;
                break;
            case DEVICE_2_MAC:
                devID = 2;
                break;
            case DEVICE_3_MAC:
                devID = 3;
                break;
        }
        return devID;
    }

    private void broadcastUpdate(final String action,
                                 final BluetoothGattCharacteristic characteristic,
                                 final String UUID) {
        final Intent intent = new Intent(action);
            int devID = 0;
            switch (UUID) {
                case DEVICE_1_MAC:
                    devID = 1;
                    break;
                case DEVICE_2_MAC:
                    devID = 2;
                    break;
                case DEVICE_3_MAC:
                    devID = 3;
                    break;
            }


            final byte[] data = characteristic.getValue();

            intent.putExtra(EXTRA_DATA, data);
            intent.putExtra(DEVICEID,devID);
        sendBroadcast(intent);
    }

    public class LocalBinder extends Binder {
        BluetoothLeService getService() {
            return BluetoothLeService.this;
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        Log.i(TAG, "onBind: BINDED");
        return mBinder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        // After using a given device, you should make sure that BluetoothGatt.close() is called
        // such that resources are cleaned up properly.  In this particular example, close() is
        // invoked when the UI is disconnected from the Service.
        close();
        return super.onUnbind(intent);
    }

    private final IBinder mBinder = new LocalBinder();

    /**
     * Initializes a reference to the local Bluetooth adapter.
     *
     * @return Return true if the initialization is successful.
     */
    public boolean initialize() {
        // For API level 18 and above, get a reference to BluetoothAdapter through
        // BluetoothManager.
        if (mBluetoothManager == null) {
            mBluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
            if (mBluetoothManager == null) {
                Log.e(TAG, "Unable to initialize BluetoothManager.");
                return false;
            }
        }

        mBluetoothAdapter = mBluetoothManager.getAdapter();
        if (mBluetoothAdapter == null) {
            Log.e(TAG, "Unable to obtain a BluetoothAdapter.");
            return false;
        }

        return true;
    }

    /**
     * Connects to the GATT server hosted on the Bluetooth LE device.
     *
     * @param address The device address of the destination device.
     *
     * @return Return true if the connection is initiated successfully. The connection result
     *         is reported asynchronously through the
     *         {@code BluetoothGattCallback#onConnectionStateChange(android.bluetooth.BluetoothGatt, int, int)}
     *         callback.
     */
    public boolean connect(int device_ID) {
        final String address = getDeviceMac(device_ID);
        Log.i(TAG, "Connecting to " + address);
        BluetoothGatt mBluetoothGatt = mBluetoothGattList[device_ID-1];
        if (mBluetoothAdapter == null || address == null) {
            Log.w(TAG, "BluetoothAdapter not initialized or unspecified address.");
            return false;
        }

        // Previously connected device.  Try to reconnect.
        if ( mBluetoothGatt != null) {
            Log.d(TAG, "Trying to use an existing mBluetoothGatt for connection.");
            if (mBluetoothGatt.connect()) {
                mConnectionStateList[device_ID-1] = STATE_CONNECTING;
                return true;
            } else {
                return false;
            }
        }

        final BluetoothDevice device = mBluetoothAdapter.getRemoteDevice(address);
        if (device == null) {
            Log.w(TAG, "Device not found.  Unable to connect.");
            return false;
        }
        // We want to directly connect to the device, so we are setting the autoConnect
        // parameter to false.
        mBluetoothGattList[device_ID-1] = device.connectGatt(this, false, mGattCallback);
        Log.d(TAG, "Trying to create a new connection.");
        mBluetoothDeviceAddress_Device1 = address;
        mConnectionStateList[device_ID-1] = STATE_CONNECTING;

        return true;
    }

    /**
     * Disconnects an existing connection or cancel a pending connection. The disconnection result
     * is reported asynchronously through the
     * {@code BluetoothGattCallback#onConnectionStateChange(android.bluetooth.BluetoothGatt, int, int)}
     * callback.
     */
    public void disconnect(int device_ID) {
        BluetoothGatt mBluetoothGatt = mBluetoothGattList[device_ID-1];
        if (mBluetoothAdapter == null || mBluetoothGatt == null) {
            Log.w(TAG, "BluetoothAdapter not initialized");
            return;
        }
        mBluetoothGatt.disconnect();
    }

    /**
     * After using a given BLE device, the app must call this method to ensure resources are
     * released properly.
     */
    public void close() {
        for(int i = 0; i <3; i++){
            if ( mBluetoothGattList[i] == null) {
                return;
            }
            mBluetoothGattList[i].close();
            mBluetoothGattList[i] = null;
        }

    }

    /**
     * Request a read on a given {@code BluetoothGattCharacteristic}. The read result is reported
     * asynchronously through the {@code BluetoothGattCallback#onCharacteristicRead(android.bluetooth.BluetoothGatt, android.bluetooth.BluetoothGattCharacteristic, int)}
     * callback.
     *
     * @param characteristic The characteristic to read from.
     */
    public void readCharacteristic(BluetoothGattCharacteristic characteristic, int device_ID) {
        if (mBluetoothAdapter == null || mBluetoothGattList[device_ID-1] == null) {
            Log.w(TAG, "BluetoothAdapter not initialized");
            return;
        }
        mBluetoothGattList[device_ID-1].readCharacteristic(characteristic);
    }

    /**
     * Enables or disables notification on a give characteristic.
     *
     * @param characteristic Characteristic to act on.
     * @param enabled If true, enable notification.  False otherwise.
     */
    public void setCharacteristicNotification(BluetoothGattCharacteristic characteristic,
                                              boolean enabled, int device_ID) {
        if (mBluetoothAdapter == null || mBluetoothGattList[device_ID-1] == null) {
            Log.w(TAG, "BluetoothAdapter not initialized");
            return;
        }
        mBluetoothGattList[device_ID-1].setCharacteristicNotification(characteristic, enabled);

        // This is specific to Heart Rate Measurement.
//        if (UUID_HEART_RATE_MEASUREMENT.equals(characteristic.getUuid())) {
//            BluetoothGattDescriptor descriptor = characteristic.getDescriptor(
//                    UUID.fromString(SampleGattAttributes.CLIENT_CHARACTERISTIC_CONFIG));
//            descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
//            mBluetoothGatt.writeDescriptor(descriptor);
//        }
    }

    /**
     * Retrieves a list of supported GATT services on the connected device. This should be
     * invoked only after {@code BluetoothGatt#discoverServices()} completes successfully.
     *
     * @return A {@code List} of supported services.
     */
    public List<BluetoothGattService> getSupportedGattServices(int device_ID) {
        if (mBluetoothGattList[device_ID-1] == null) return null;

        return mBluetoothGattList[device_ID-1].getServices();
    }

    public BluetoothGattCharacteristic extact_serialCharacteristic(List<BluetoothGattService> gattServices){
        if (gattServices == null) return null;
        for (BluetoothGattService gattService : gattServices) {
            List<BluetoothGattCharacteristic> gattCharacteristics = gattService.getCharacteristics();
            // Loops through available Characteristics.
            for (BluetoothGattCharacteristic gattCharacteristic : gattCharacteristics) {
                if (gattCharacteristic.getUuid().toString().equals(SERIAL_PORT_UUID)){
                    return gattCharacteristic;
                };
            }
        }
        return null;
    }
}

