package com.example.blecapstone;

import android.app.Activity;
import android.os.SystemClock;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

import static java.util.concurrent.Executors.newFixedThreadPool;

public class NetworkThread {
    public static final String TAG = "CAPSTONE_BLE_NETWORK";

    private static BlockingQueue<byte[]> sendQueue;
    public static java.net.Socket Socket;
    public static DataOutputStream SockStream;
    public static String SERVER_IP = "192.168.1.100"; //server IP address
    public static int SERVER_PORT = 4321;
    private static InetAddress SERV_INET;

    //Dirty Dirty Singleton
    private static NetworkThread instance;
    public static boolean isRunning;
    public static boolean isKill = false;

    public static NetworkThread getGetInstance() {
        return instance;
    }

    //ThreadingStuff
    private static ExecutorService executorService;

    public NetworkThread() {
        instance = this;
        sendQueue = new LinkedBlockingQueue<>(100);
        executorService = newFixedThreadPool(2);
    }

    public static byte[] makeDataFrame(
            final int DEVICEID,
            final byte[] AccelGyroData
    ){
        ByteBuffer frame = ByteBuffer.allocate(1 + 1 + 6);
        frame.put((byte)DEVICEID);
        frame.put(AccelGyroData);
        return frame.array();
    }

    public static void pushFrame(
            final byte[] frame
    ){
        sendQueue.offer(frame);
    }
    public static void startnetworkTask() {

        executorService.execute(new Runnable() {
            @Override
            public void run() {
                while (!isKill) {
                    try {
                        isRunning = true;
                        Log.i(TAG, "Connecting to Server");
                        InetAddress serverAddr = InetAddress.getByName(SERVER_IP);
                        java.net.Socket socket = new Socket(serverAddr, SERVER_PORT);
                        Log.i(TAG, "Connected to Server!!!!");
                        DataOutputStream sockStream = new DataOutputStream(
                                new BufferedOutputStream(
                                        socket.getOutputStream()
                                )
                        );
                        int i;
                        while (!isKill) {
                            if (!sendQueue.isEmpty()) {
                                for (i = 0; i < sendQueue.size(); i++) {
                                    sockStream.write(sendQueue.take());
                                }
                                sockStream.flush();
                            }
                        }

                        socket.close();
                    } catch (UnknownHostException e) {
                        Log.e(TAG, "sendBufferedFrames: UnknownHostException... Retrying");
                    } catch (IOException e) {
                        Log.e(TAG, "sendBufferedFrames: IOException... Retrying");
                        SystemClock.sleep(5000);
                    } catch (InterruptedException e) {
                        Log.e(TAG, "sendBufferedFrames: InterruptedException", e);
                        isKill = true;
                        e.printStackTrace();
                    } finally {
                        isRunning = false;
                    }

                }
            }
        });
    }

}
