import serial
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec
import numpy as np
from threading import Thread
from queue import Queue
import socketserver
import struct
import socketserver
import struct


_LIMIT = 16384


# definitons
frameDecode = struct.Struct("!Bbbbbbbb")
buffersize = frameDecode.size * 100
NUMVIEWSAMPLES = 300

class DeviceDataBuffer():
    def __init__(self):
        self.a_xList = []
        self.a_yList = []
        self.a_zList = []

        self.g_xList = []
        self.g_yList = []
        self.g_zList = []
        
        self.RMSList = []
        self.MAVList = []
        self.ZCSList = []

        self.activation_List = []
        self.activationFlag = False
        self.readyFlag = False
        self.activeCooldown = 0

        self.gravityQuarrel = [[0,0,0,1,1,1]]

        for i in range(NUMVIEWSAMPLES):
            self.a_xList.append(0)
            self.a_yList.append(0)
            self.a_zList.append(0)

            self.g_xList.append(0)
            self.g_yList.append(0)
            self.g_zList.append(0)

            self.activation_List.append(0)

            self.RMSList.append(0)
            self.MAVList.append(0)
            self.ZCSList.append(0)
            
    def updateMyoware(self,R,M,Z):
        self.RMSList.pop(0)
        self.MAVList.pop(0)
        self.ZCSList.pop(0) 
        self.RMSList.append(R)
        self.MAVList.append(M)
        self.ZCSList.append(Z)

    def updatePlots(self,aX,aY,aZ, gX,gY,gZ):
        def recentlyActive(Threshold):
            return 2 in self.activation_List[-Threshold:]
        def update_activation(coords):
            THRESHOLD_ACTIVATION = 0.3
            RECENT_ACTIVATION_THRESHOLD = 10
            COOLDOWN_THRESHOLD = 5
            GRAVITY_THRESHOLD = 0.2
            GRAVITY_Z = -1.0
            
            magnitude = (coords[0]**2 +coords[1]**2 +coords[2]**2)**(0.5)
            # Print Magnitude - gravity??
            # print(magnitude-1)

            
            # StartOfMoveDetection
            if (not self.activationFlag):
                # IF not currently doing a move
                if abs( coords[2] - (GRAVITY_Z) ) < GRAVITY_THRESHOLD and (not recentlyActive(RECENT_ACTIVATION_THRESHOLD)):
                    self.readyFlag = True
                else:
                    self.readyFlag = False


                if abs(magnitude - 1) > THRESHOLD_ACTIVATION and self.readyFlag:
                    self.activationFlag = True
                    self.activeCooldown = COOLDOWN_THRESHOLD
                    print("ACTIVE!!!!")
            else:
                # IF currently doing a move
                self.readyFlag = False
                self.activeCooldown-=1
                if abs(magnitude - 1) > THRESHOLD_ACTIVATION:
                    self.activationFlag = True
                    self.activeCooldown = COOLDOWN_THRESHOLD
                elif self.activeCooldown <= 0 and abs( coords[2] - (GRAVITY_Z) ) < GRAVITY_THRESHOLD:
                    self.activationFlag = False
            
            # calculating Activation Value
            # 2 == Activated
            # 1 == Ready
            # 0 == Idle

            updateValue = 0
            if self.readyFlag:
                updateValue = 1
            if self.activationFlag:
                updateValue = 2
            self.activation_List.pop(0)
            self.activation_List.append(updateValue)

        
        def movingAverage(coords):
        # moving AVG Filter 
            NEWWEIGHT = 0.4 #Incoming Data Weightage
            OLDWEIGHT = 1 - NEWWEIGHT #Previous Data Weightage

            coords[0] = coords[0]*NEWWEIGHT + self.a_xList[-1]*OLDWEIGHT
            coords[1] = coords[1]*NEWWEIGHT + self.a_yList[-1]*OLDWEIGHT
            coords[2] = coords[2]*NEWWEIGHT + self.a_zList[-1]*OLDWEIGHT
            return coords

        coords = list(
            map(lambda x: int(x)/64,[aX,aY,aZ]))
        rotations = list(
            map(lambda x: (int(x)/128 * 250) ,[gX,gY,gZ]))

        movingAverage(coords)
        update_activation(coords)

        self.gravityQuarrel[0] = coords

        self.a_xList.pop(0)
        self.a_yList.pop(0)
        self.a_zList.pop(0)

        self.g_xList.pop(0)
        self.g_yList.pop(0)
        self.g_zList.pop(0)

        self.a_xList.append(coords[0])
        self.a_yList.append(coords[1])
        self.a_zList.append(coords[2])

        self.g_xList.append(rotations[0])
        self.g_yList.append(rotations[1])
        self.g_zList.append(rotations[2])


DEV1_PLOT_BUFFER = DeviceDataBuffer()
DEV2_PLOT_BUFFER = DeviceDataBuffer()
DEV3_PLOT_BUFFER = DeviceDataBuffer()

PLOT_BUFFER_LIST = [DEV1_PLOT_BUFFER,DEV2_PLOT_BUFFER,DEV3_PLOT_BUFFER]

# serverstuff
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        buf = bytearray()

        print("connected!")
        while(True):
            data = self.request.recv(buffersize)
            if data == b'':
                break
            buf.extend(data)
            while(len(buf) > frameDecode.size):
                # ts, depthsize ,rbgsize = tsDecode.unpack(buf[:tsDecode.size])
                DeviceID, reserved, aX,aY,aZ, gX,gY,gZ = frameDecode.unpack(buf[:frameDecode.size])
                buf = buf[frameDecode.size:]
                # print(DeviceID, aX,aY,aZ, gX,gY,gZ)
                
                if (DeviceID > 3) or (DeviceID < 1):
                    continue
                else:
                    PLOT_BUFFER_LIST[DeviceID-1].updatePlots(aX,aY,aZ, gX,gY,gZ)
                

        print("connectio Closed")



def runServer():
    ser = serial.Serial('COM3', 115200, timeout=2)
    while(True):
        l = ser.readline()
        decoded = l.decode().split()
        print(decoded)
        if decoded[0] == 'a':
            aX,aY,aZ, gX,gY,gZ = list(map(lambda x: str(x),decoded[1:]))
            PLOT_BUFFER_LIST[0].updatePlots(aX,aY,aZ, gX,gY,gZ)
        elif decoded[0] == 'b':
            rms, mav,zcr = list(map(lambda x: float(x),decoded[1:]))
            PLOT_BUFFER_LIST[0].updateMyoware(rms, mav,zcr)

# Displaystuff



def updateThreadforPlots():
    def configurePlots(index,accel,gyro,activation,rms,mav,zcr,deviceData, deviceID):
        activation.set_title("Device " + str(deviceID) + "\nActivation" )
        accel.set_title("Accel" )
        gyro.set_title("Gyro" )
        rms.set_title("rms" )
        mav.set_title("mav" )
        zcr.set_title("zcr" )

        # TODO plot the activation

        ax1, = accel.plot(index, deviceData.a_xList, label = "X")
        ax2, = accel.plot(index, deviceData.a_yList, label = "Y")
        ax3, = accel.plot(index, deviceData.a_zList, label = "Z")

        ax4, = gyro.plot(index, deviceData.g_xList, label = "X")
        ax5, = gyro.plot(index, deviceData.g_yList, label = "Y")
        ax6, = gyro.plot(index, deviceData.g_zList, label = "Z")

        ax7, = activation.plot(index, deviceData.activation_List, label = "R")

        ax8, = rms.plot(index, deviceData.RMSList, label = "RMS")
        ax9, = mav.plot(index, deviceData.MAVList, label = "mav")
        ax10, = zcr.plot(index, deviceData.ZCSList, label = "zcr")

        
        rms.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        rms.set_ylim(ymin = 0 , ymax = 40 )

        mav.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        mav.set_ylim(ymin = 0 , ymax = 40 )

        zcr.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        zcr.set_ylim(ymin = 0 , ymax = 100 )

        activation.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        activation.set_ylim(ymin = 0.2 , ymax = 2.2 )

        accel.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        accel.set_ylim(ymin = -2 , ymax = 2 )

        gyro.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        gyro.set_ylim(ymin = -250 , ymax = 250 )

        # if deviceID == 3:
        #     accel.legend((ax1, ax2, ax3), ('X', 'Y', 'Z'), loc ='upper left', bbox_to_anchor=(1.05, 1),fontsize='xx-small' )
        #     gyro.legend((ax4, ax5, ax6), ('X', 'Y', 'Z'), loc ='upper left', bbox_to_anchor=(1.05, 1),fontsize='xx-small')

        return [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10]

    def updatePlotData(plotAxis,deviceData):
        ax1,ax2,ax3,ax4,ax5,ax6, ax7,ax8,ax9,ax10 = plotAxis
        ax1.set_data(index, deviceData.a_xList)
        ax2.set_data(index, deviceData.a_yList)
        ax3.set_data(index, deviceData.a_zList)

        ax4.set_data(index, deviceData.g_xList)
        ax5.set_data(index, deviceData.g_yList)
        ax6.set_data(index, deviceData.g_zList)

        ax7.set_data(index, deviceData.activation_List)

        ax8.set_data(index, deviceData.RMSList)
        ax9.set_data(index, deviceData.MAVList)
        ax10.set_data(index, deviceData.ZCSList)



    index = []
    for i in range(NUMVIEWSAMPLES):
        index.append(i)

    try:
        # GRav
        # fig = plt.figure(2)
        # ax = fig.gca(projection='3d')
        # Vec = ax.quiver(0,0,0,1,1,1)
        # ax.set_xlim(-1, 1)
        # ax.set_ylim(-1, 1)
        # ax.set_zlim(-1, 1)
        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')


        # Accel
        fig2 = plt.figure(1)
        gs = gridspec.GridSpec(3, 3, width_ratios=[1,1,1], height_ratios=[0.2,1,1]) 

        # DEV1_accel = fig2.add_subplot(231)
        # DEV2_accel = fig2.add_subplot(232)
        # DEV3_accel = fig2.add_subplot(233)

        # DEV1_gyro = fig2.add_subplot(234)
        # DEV2_gyro = fig2.add_subplot(235)
        # DEV3_gyro = fig2.add_subplot(236)

        DEV1_activation = fig2.add_subplot(gs[0])

        DEV1_accel = fig2.add_subplot(gs[3])

        DEV1_RMS = fig2.add_subplot(gs[4])
        DEV1_MAV = fig2.add_subplot(gs[5])
        DEV1_ZCR = fig2.add_subplot(gs[7])

        DEV1_gyro = fig2.add_subplot(gs[6])

        DEV1_AXIS = configurePlots(index,DEV1_accel,DEV1_gyro,DEV1_activation, DEV1_RMS,DEV1_MAV,DEV1_ZCR, DEV1_PLOT_BUFFER,1)



        plt.ion()
        plt.pause(1)
        plt.show()
        while(1):
            # Grav
            # setVector(Vec, gravityQuarrel[0] )

            # accel
            updatePlotData(DEV1_AXIS,DEV1_PLOT_BUFFER)
            # updatePlotData(DEV2_AXIS,DEV2_PLOT_BUFFER)
            # updatePlotData(DEV3_AXIS,DEV3_PLOT_BUFFER)
            # axes.relim()
            # axes.autoscale_view(True,True,True)
            plt.pause(0.001)
    except Exception as a:
        print(a)
        print("exiting")
        return




def setVector(vec, coords):
    vec.set_segments([[[0,0,0],coords]])

# def updatePlots(aX,aY,aZ, gX,gY,gZ):
#     coords = list(map(lambda x: int(x)/64,[aX,aY,aZ]))
    
#     gravityQuarrel[0] = coords

#     xList.pop(0) 
#     yList.pop(0) 
#     zList.pop(0) 

#     xList.append(coords[0])
#     yList.append(coords[1])
#     zList.append(coords[2])


if __name__ == "__main__":
    uThread2 = Thread(target=updateThreadforPlots)
    uThread2.daemon = True
    uThread2.start()

    try:
        runServer()
    except KeyboardInterrupt:
        print('killing')
        sys.exit() 

    