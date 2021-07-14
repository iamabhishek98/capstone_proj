
import sys
import os
import numpy as np
from queue import Queue
import time

from predictor_ultra96 import Predictor

_LIMIT = 16384

# definitons
DANCEMOVENAMES = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")
NUMVIEWSAMPLES = 400

THRESHOLD_ACTIVATION = 0.3
RECENT_ACTIVATION_THRESHOLD = 10
COOLDOWN_THRESHOLD = 20
GRAVITY_THRESHOLD = 0.2
GRAVITY_Z = -1.0

NUMBER_OF_AFTER_SAMPLES = 5
NUMBER_OF_BEFORE_SAMPLES = 5

assert NUMBER_OF_AFTER_SAMPLES < RECENT_ACTIVATION_THRESHOLD


class DeviceDataBuffer():
    def __init__(self, name , predict = False ):
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

        self.predictor = Predictor() if predict else None

        for i in range(NUMVIEWSAMPLES):
            self.a_xList.append(0)
            self.a_yList.append(0)
            self.a_zList.append(0)

            self.g_xList.append(0)
            self.g_yList.append(0)
            self.g_zList.append(0)

            self.activation_List.append(0)
            

        
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

                    if not self.predictor == None:
                        self.predictor.startRecording()

                    print("ACTIVE!!!!")
            else:
                # IF currently doing a move
                self.readyFlag = False
                self.activeCooldown-=1
                if abs(magnitude - 1) > THRESHOLD_ACTIVATION or not (abs( coords[2] - (GRAVITY_Z) ) < GRAVITY_THRESHOLD):
                    self.activationFlag = True
                    self.activeCooldown = COOLDOWN_THRESHOLD
                elif self.activeCooldown <= 0 and abs( coords[2] - (GRAVITY_Z) ) < GRAVITY_THRESHOLD:
                    self.activationFlag = False

                    if not self.predictor == None:
                        self.predictor.stopRecording()
            
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

        coords = [aX,aY,aZ]
        rotations =[gX,gY,gZ]

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
        

        if not self.predictor==None:
            self.predictor.updateCurrentMove(self)


class DeviceDataBufferMyoWare():
    def __init__(self):
        self.RMSList = []
        self.MAVList = []
        self.ZCSList = []


        for i in range(NUMVIEWSAMPLES):
            self.RMSList.append(0)
            self.MAVList.append(0)
            self.ZCSList.append(0)
    
    
    def updatePlots(self,R,M,Z):
        self.RMSList.pop(0)
        self.MAVList.pop(0)
        self.ZCSList.pop(0) 
        self.RMSList.append(R)
        self.MAVList.append(M)
        self.ZCSList.append(Z)



class classificationEngine():
    def __init__(self):
        self.DEV1_PLOT_BUFFER = DeviceDataBuffer("dev1", predict=True)
        self.DEV2_PLOT_BUFFER = DeviceDataBuffer("dev2")
        self.DEV3_PLOT_BUFFER = DeviceDataBuffer("dev3")
        self.MYOWARE_PLOT_BUFFER = DeviceDataBufferMyoWare()

        self.PLOT_BUFFER_LIST = [self.DEV1_PLOT_BUFFER,self.DEV2_PLOT_BUFFER,self.DEV3_PLOT_BUFFER]

    def add_data(self, packet_type, d):
        if packet_type == "EMG":
            rms,mav,zcr = d
            
            self.MYOWARE_PLOT_BUFFER.updatePlots(rms,mav,zcr)
        if packet_type == "DATA":
            DeviceID,aX,aY,aZ, gX,gY,gZ = d
            DeviceID = int(DeviceID)
            self.PLOT_BUFFER_LIST[DeviceID-1].updatePlots(aX,aY,aZ, gX,gY,gZ)
            
    
        


    