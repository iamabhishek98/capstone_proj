import serial
import sys
import os
import numpy as np
from threading import Thread
from queue import Queue
import socketserver
import struct
import time
import csv
import traceback


# matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec




_LIMIT = 16384
_IS_KILL =False

# definitons
DANCEMOVENAMES = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")
frameDecode = struct.Struct("!Bbbbbbbb")
buffersize = frameDecode.size * 100
NUMVIEWSAMPLES = 400

THRESHOLD_ACTIVATION = 0.3
RECENT_ACTIVATION_THRESHOLD = 10
COOLDOWN_THRESHOLD = 5
GRAVITY_THRESHOLD = 0.2
GRAVITY_Z = -1.0

BASEPATH = os.getcwd()
SAVEFOLDER = 'savedMoves'
NUMBER_OF_AFTER_SAMPLES = 5
NUMBER_OF_BEFORE_SAMPLES = 5

assert NUMBER_OF_AFTER_SAMPLES < RECENT_ACTIVATION_THRESHOLD


def recordButtonCallbackGenerator(list_of_data_collectors):
    def callback(e):
        for dc in list_of_data_collectors:
            dc.startRecording()
    return callback

def stopButtonCallbackGenerator(list_of_data_collectors):
    def callback(e):
        for dc in list_of_data_collectors:
            dc.stopRecording()
    return callback

def radioBoxSubmitCallbackGenerator(list_of_data_collectors):
    def callback(text):
        for dc in list_of_data_collectors:
            dc.currentMove = text
    return callback


class DataCollector():

    def __init__(self,name):  
        self.name = name 
        self.currentMove = "defaultMove"
        self.isRecording = False
        self.samplesRecorded = 0

        # internal Buffers | separate from others
        self.a_xList = []
        self.a_yList = []
        self.a_zList = []

        self.g_xList = []
        self.g_yList = []
        self.g_zList = []
        
        self.activation_List = []
    
    def clearBuffers(self):
        self.a_xList = []
        self.a_yList = []
        self.a_zList = []

        self.g_xList = []
        self.g_yList = []
        self.g_zList = []
        
        self.activation_List = []

    def startRecording( self ):
        print("Recording Started For {} on {}".format(self.name, self.currentMove))
        self.isRecording = True
    
    def stopRecording( self ):
        if self.samplesRecorded == 0:
            print("Recording Cancelled For {} on {}".format(self.name, self.currentMove))
            return None
        self.saveRecording()
        self.isRecording = False
        self.samplesRecorded = 0
        self.clearBuffers()

    def updateCurrentMove(self,databuffer):
        if self.isRecording:
            self.samplesRecorded +=1

            self.a_xList.append(databuffer.a_xList[-1])
            self.a_yList.append(databuffer.a_yList[-1])
            self.a_zList.append(databuffer.a_zList[-1])

            self.g_xList.append(databuffer.g_xList[-1])
            self.g_yList.append(databuffer.g_yList[-1])
            self.g_zList.append(databuffer.g_zList[-1])
        
            self.activation_List.append(databuffer.activation_List[-1])

    def saveRecording(self):
        timeNow = round(time.time() * 10000)
        fName = self.name + "_" + self.currentMove + "_" + str(timeNow)
        savePath = os.path.join(BASEPATH,SAVEFOLDER, fName)
        if not os.path.exists(os.path.dirname(savePath)):
            try:
                os.makedirs(os.path.dirname(savePath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(savePath, 'w', newline='') as csvfile:
            row = [
                    'a_xList',
                    'a_yList',
                    'a_zList',
                    'g_xList',
                    'g_yList',
                    'g_zList',
                    'activation_List'
                ]
            csvWriter = csv.writer(csvfile, delimiter=',')
            csvWriter.writerow(row)
            for idx in range(len(self.a_xList)):
                row = [
                    self.a_xList[idx],
                    self.a_yList[idx],
                    self.a_zList[idx],
                    self.g_xList[idx],
                    self.g_yList[idx],
                    self.g_zList[idx],
                    self.activation_List[idx]
                ] 
                csvWriter.writerow(row)
            print("Recording saved as {}. Saved {} samples".format(fName, self.samplesRecorded))
    

class DeviceDataBuffer():
    def __init__(self, name):
        self.name = name
        self.a_xList = []
        self.a_yList = []
        self.a_zList = []

        self.g_xList = []
        self.g_yList = []
        self.g_zList = []
        
        self.activation_List = []
        self.activationFlag = False
        self.readyFlag = False
        self.activeCooldown = 0

        self.gravityQuarrel = [[0,0,0,1,1,1]]

        self.recordingBuffer = []
        self.recording = False

        self.DC = DataCollector(self.name)

        for i in range(NUMVIEWSAMPLES):
            self.a_xList.append(0)
            self.a_yList.append(0)
            self.a_zList.append(0)

            self.g_xList.append(0)
            self.g_yList.append(0)
            self.g_zList.append(0)

            self.activation_List.append(0)
            
    def getDC(self):
        return self.DC
        
    def updatePlots(self,aX,aY,aZ, gX,gY,gZ):
        def recentlyActive(Threshold):
            return 2 in self.activation_List[-Threshold:]
        
        def update_activation(coords):

            
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

        self.DC.updateCurrentMove(self)


DEV1_PLOT_BUFFER = DeviceDataBuffer("dev1")
DEV2_PLOT_BUFFER = DeviceDataBuffer("dev2")
DEV3_PLOT_BUFFER = DeviceDataBuffer("dev3")

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
    HOST, PORT = "192.168.1.100", 4321
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("Host: " + str(HOST) + " on port: " + str(PORT))
        server.timeout = 3
        server.serve_forever()


# Displaystuff



def updateThreadforPlots():
    def configurePlots(index,accel,gyro,activation,deviceData, deviceID):
        activation.set_title("Device " + str(deviceID) + "\nActivation" )
        accel.set_title("Accel" )
        gyro.set_title("Gyro" )

        # TODO plot the activation

        ax1, = accel.plot(index, deviceData.a_xList, label = "X")
        ax2, = accel.plot(index, deviceData.a_yList, label = "Y")
        ax3, = accel.plot(index, deviceData.a_zList, label = "Z")

        ax4, = gyro.plot(index, deviceData.g_xList, label = "X")
        ax5, = gyro.plot(index, deviceData.g_yList, label = "Y")
        ax6, = gyro.plot(index, deviceData.g_zList, label = "Z")

        ax7, = activation.plot(index, deviceData.activation_List, label = "R")
        

        activation.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        activation.set_ylim(ymin = 0.2 , ymax = 2.2 )

        accel.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        accel.set_ylim(ymin = -2 , ymax = 2 )

        gyro.set_xlim(xmin = 0 , xmax = NUMVIEWSAMPLES )
        gyro.set_ylim(ymin = -250 , ymax = 250 )

        if deviceID == 3:
            accel.legend((ax1, ax2, ax3), ('X', 'Y', 'Z'), loc ='upper left', bbox_to_anchor=(1.05, 1),fontsize='xx-small' )
            gyro.legend((ax4, ax5, ax6), ('X', 'Y', 'Z'), loc ='upper left', bbox_to_anchor=(1.05, 1),fontsize='xx-small')

        return [ax1,ax2,ax3,ax4,ax5,ax6,ax7]

    def updatePlotData(plotAxis,deviceData):
        ax1,ax2,ax3,ax4,ax5,ax6, ax7 = plotAxis
        ax1.set_data(index, deviceData.a_xList)
        ax2.set_data(index, deviceData.a_yList)
        ax3.set_data(index, deviceData.a_zList)

        ax4.set_data(index, deviceData.g_xList)
        ax5.set_data(index, deviceData.g_yList)
        ax6.set_data(index, deviceData.g_zList)

        ax7.set_data(index, deviceData.activation_List)



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

        axRecord = fig2.add_axes([0.7, 0.02, 0.1, 0.075])
        axStop = fig2.add_axes([0.81, 0.02, 0.1, 0.075])
        axText = fig2.add_axes([0.01, 0.02, 0.1, 0.2])

        listDC = list(map(lambda x: x.getDC(),PLOT_BUFFER_LIST ))
        bRecord = Button(axRecord, 'Record')
        bRecord.on_clicked(recordButtonCallbackGenerator(listDC))
        bStop = Button(axStop, 'Stop')
        bStop.on_clicked(stopButtonCallbackGenerator(listDC))
        radioB= RadioButtons(axText, DANCEMOVENAMES)
        radioB.on_clicked(radioBoxSubmitCallbackGenerator(listDC))

        DEV1_activation = fig2.add_subplot(gs[0])
        DEV2_activation  = fig2.add_subplot(gs[1])
        DEV3_activation  = fig2.add_subplot(gs[2])

        DEV1_accel = fig2.add_subplot(gs[3])
        DEV2_accel = fig2.add_subplot(gs[4])
        DEV3_accel = fig2.add_subplot(gs[5])

        DEV1_gyro = fig2.add_subplot(gs[6])
        DEV2_gyro = fig2.add_subplot(gs[7])
        DEV3_gyro = fig2.add_subplot(gs[8]) 

        DEV1_AXIS = configurePlots(index,DEV1_accel,DEV1_gyro,DEV1_activation,DEV1_PLOT_BUFFER,1)
        DEV2_AXIS = configurePlots(index,DEV2_accel,DEV2_gyro,DEV2_activation,DEV2_PLOT_BUFFER,2)
        DEV3_AXIS = configurePlots(index,DEV3_accel,DEV3_gyro,DEV3_activation,DEV3_PLOT_BUFFER,3)


        plt.ion()
        plt.pause(1)
        plt.show()
        while(not _IS_KILL):
            # Grav
            # setVector(Vec, gravityQuarrel[0] )

            # accel
            updatePlotData(DEV1_AXIS,DEV1_PLOT_BUFFER)
            updatePlotData(DEV2_AXIS,DEV2_PLOT_BUFFER)
            updatePlotData(DEV3_AXIS,DEV3_PLOT_BUFFER)
            # axes.relim()
            # axes.autoscale_view(True,True,True)
            plt.pause(0.001)
        plt.close('all')
        print("Gracefull Exit")
    except Exception as a:
        traceback.print_exc()
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
        _IS_KILL = True

        time.sleep(1)

        print('killing')
        sys.exit() 

    