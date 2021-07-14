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
from collections import Counter as libCounter


# =======GLOBALS=======
_IS_KILL = False
_IS_MAIN = __name__ == "__main__"

### ===========BASE CONFIG=============== ###
BASEPATH = os.getcwd()
SAVE_FOLDER_NAME_DATARECORDER = 'savedMoves'
DANCEMOVENAMES = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")

headerDecode= struct.Struct("!Bb")
frameDecode = struct.Struct("!bbbbbb")
myowareDecode = struct.Struct("<HHH")
buffersize = frameDecode.size * 100

IS_RUNNING_ON_ULTRA =True
IS_CONNECT_TO_ULTRA =True
IS_DATA_RECORDER =True
IS_PREDICTOR = False
IS_IN_PASSTHROUGH_MODE = False
SOLO_TEST_MODE = False

# ===========Setting settings from OS===========
_platform = sys.platform
if _platform == "win32":
    print("RUNNING LOCALLY")
    IS_RUNNING_ON_ULTRA =False
    IS_CONNECT_TO_ULTRA =IS_CONNECT_TO_ULTRA
    IS_DATA_RECORDER =False
    IS_PREDICTOR = False
    IS_IN_PASSTHROUGH_MODE = IS_IN_PASSTHROUGH_MODE

elif _platform == "linux":
    IS_RUNNING_ON_ULTRA =True
    IS_CONNECT_TO_ULTRA =False
    IS_DATA_RECORDER =True
    IS_PREDICTOR = True
    IS_IN_PASSTHROUGH_MODE = False
    _IS_MAIN = True
    
else:
    print("UNKNOWN PLATFORM")
    assert False


    

### ===========DATABUFFER CONFIG=============== ###
# conenction timeout
MIN_SAMPLES_BEFORE_TIMEOUT = 60
# Internal buffer size
DATA_BUFFER_INTERNAL_BUFFER_SIZE = 400
# Constants for the moving average filter
NEWWEIGHT = 0.4 #Incoming Data Weightage
OLDWEIGHT = 1 - NEWWEIGHT #Previous Data Weightage
# The magnitude of the ideal gravity vector for the Z axis
GRAVITY_Z = -1.0
# The magnitude of the ideal gravity vector combined axis
GRAVITY_TRUE_MAG = 1
# The Threshold under which hand_in_idle_position is true
GRAVITY_THRESHOLD = 0.3
# The Threshold under which hand_in_idle_position_return is true
GRAVITY_THRESHOLD_END = 0.2
# The number of samples to look back for activity
RECENT_ACTIVATION_THRESHOLD = 5
# The Threshold above which is_large_movement is true
THRESHOLD_ACTIVATION = 0.4
# The Threshold above which is_small_movement is true
THRESHOLD_ACTIVATION_SMALL= 0.3
# the number of samples after an activation that a move will timeout if nothing happens
MOVE_TIMEOUT_MAX_SHORT = 5
# the number of samples after an activation that a move will timeout if nothing happens
MOVE_TIMEOUT_MAX_MEDIUM = 5
# the number of samples after an activation that a move will timeout if nothing happens
MOVE_TIMEOUT_MAX_LONG = 40
# number of samples that after which a dance move is most likely
MINIMUM_LARGE_MOVE_TIME = 20
# Number of samples to be ready for
READY_VALIDITY_SAMPLES = 5
# Number of pre-buffered samples to add to prediction Buffer
PREDICTION_PRE_SAMPLES = 6
# Number of samples per prediction window
MAX_SAMPLES = 100
# If True, will send prediction when PREDICTION_SAMPLES is reached
USE_PREDICTION_SAMPLES =True
# Number of Dance samples required before triggering Prediction
PREDICTION_SAMPLES = 100
# Minimum samples required for prediction
MIN_MOVE_TIME_SAMPLES =99
# Minimum consequitive high samples required for prediction
CONSEC_HIGH_DANCE_THRESH = 0
# The Threshold for finisher
FINISHER_GRAVITY_THRESHOLD = 0.1
# The Threshold for finisher numeber of samples
FINISHER_MOVE_MIN_SAMPLES = 40

#maxium Sync Delay in seconds
MAX_SYNC = 2

# Thresholds for turning
RIGHT_TURN_THRESH = 100
LEFT_TURN_THRESH = -100
TURN_LOCKOUT_SAMPLES = 20
TURN_VALIDITY_MAX_SAMPLES  = 1000
CONSEC_HIGH_TURN_THRESH = 5
ANTI_SHAKE_COOLDOWN =5

# Prediction Timeout
PREDICTION_ENSEMBLE_MAX_COUNT_VALID = 1000

# If imported by anotherModule, define IMPORTED_BY_OTHER_MOD =True
if not _IS_MAIN:
    print("+++++++++++++++++++++++++++++++++++")
    IS_RUNNING_ON_ULTRA =False
    IS_CONNECT_TO_ULTRA =False
    IS_DATA_RECORDER =False
    IS_PREDICTOR = False
    IS_IN_PASSTHROUGH_MODE = False
    USE_PREDICTION_SAMPLES =False

# This class stores and buffers and processes the data from 1 bluetooth device
class DeviceDataBuffer():
    DEV_NAME_TO_EXT_COMMS_ID = {
        "dev1": 1,
        "dev2": 2,
        "dev3": 3,
        "Myo": "Myo"
    }
    def __init__(self, deviceName,
        internalBufferSize = DATA_BUFFER_INTERNAL_BUFFER_SIZE,
        isRunningOnUltra = False,
        connectionToUltra = None, 
        initDataRecording = False,
        predictor = False,
        turnEventCallback = None,
        predictionEventCallback  = None
        ):
        # declaration of internal state/attributes
        self.deviceName = deviceName
        self.isUltra96 = isRunningOnUltra
        self.connectionToUltra = connectionToUltra
        self.internalBufferSize = internalBufferSize
        self.transmitToUltra = False
        # ===Data===
        self.aX = []
        self.aY = []
        self.aZ = []
        self.gX = []
        self.gY = []
        self.gZ = []

        self.actList = []

        # self.data_list = [aX,aY,aZ,gX,gY,gZ,actList]

        # ===Flags===
        self.is_dancing = False
        self.is_ready = False
        self.is_hand_idle = False
        self.is_hand_high = False
        self.is_recent_dance = False
        self.is_large_movement = False
        self.is_small_movement =False
        self.is_turn_cooldown = False
        self.is_connected = False
        self.is_current_move_valid = True


        # ===counters===
        self.count_connection_timeout = 0
        self.count_move_timeout = 0
        self.count_move_total_duration = 0
        self.count_turn_lockout = 0
        self.count_consecutive_high_turns = 0
        self.count_consecutive_high_energy = 0
        self.count_above_left_threshold_timout = 0
        self.count_above_right_threshold_timout = 0
        self.count_ready_valid = 0
        self.count_consecutive_hand_high = 0


        
        # Initialse data recording module
        if initDataRecording:
            self.recordingModule = DataRecorder(self)
        else:
            self.recordingModule = None

        # Initialse internal data buffers
        self.initInternalBuffers()

        # Set prediction Engine
        if predictor == None:
            self.predictor = predictor
        else:
            self.predictor = predictorBuffer(self,predictor)

        # Turn Engine callback
        self.turnEventCallback = turnEventCallback
        self.predictionEventCallback = predictionEventCallback
    
    # ========STATE MANAGEMENT FUNCTIONS==========
    # Initialse initial values for internal Buffers
    def initInternalBuffers(self):
        # === DATA ===
        self.aX = [0] * self.internalBufferSize
        self.aY = [0] * self.internalBufferSize
        self.aZ = [0] * self.internalBufferSize
        self.gX = [0] * self.internalBufferSize
        self.gY = [0] * self.internalBufferSize
        self.gZ = [0] * self.internalBufferSize
        self.actList = [0] * self.internalBufferSize

        # ===Flags===
        self.is_dancing = False
        self.is_ready = False
        self.is_hand_idle = False
        self.is_recent_dance = False
        self.is_large_movement = False

        # ===Counters===
        self.count_move_timeout = 0
        self.count_move_total_duration = 0
        


    def updateInternalState(self,aX,aY,aZ,gX,gY,gZ):
        # Update Connection watchdog and status
        self.count_connection_timeout = MIN_SAMPLES_BEFORE_TIMEOUT
        if not self.is_connected:
            print("Device {} connected!".format(self.deviceName))
        self.is_connected = True

        # Only Normalise if running on the relay device
        if not _IS_MAIN:
            aX_norm,aY_norm,aZ_norm  = aX,aY,aZ
            gX_norm,gY_norm,gZ_norm  = gX,gY,gZ
        elif not self.isUltra96:
            aX_norm,aY_norm,aZ_norm  = self.calculateNormalizedAcceleration(aX,aY,aZ)
            gX_norm,gY_norm,gZ_norm  = self.calculateNormalizedGyroscope(gX,gY,gZ)
        elif self.isUltra96:
            aX_norm,aY_norm,aZ_norm  = aX,aY,aZ
            gX_norm,gY_norm,gZ_norm  = gX,gY,gZ

        # calculating Magnitude
        aMag = self.calculateAccelMagnitude(aX_norm,aY_norm,aZ_norm)

        # Moving average Filter
        if _IS_MAIN:
            aX_norm,aY_norm,aZ_norm = self.calculateMovingAverage(aX_norm,aY_norm,aZ_norm,gX_norm,gY_norm,gZ_norm)

        # calculating Per sample flags
        self.is_hand_idle = abs(aZ_norm - (GRAVITY_Z) ) < GRAVITY_THRESHOLD
        self.is_hand_returned_to_idle = abs(aZ_norm - (GRAVITY_Z) ) < GRAVITY_THRESHOLD_END
        self.is_recent_dance = 2 in self.actList[-RECENT_ACTIVATION_THRESHOLD:]
        self.is_large_movement = abs(aMag - GRAVITY_TRUE_MAG) > THRESHOLD_ACTIVATION
        self.is_small_movement = abs(aMag - GRAVITY_TRUE_MAG) > THRESHOLD_ACTIVATION_SMALL
        self.is_ready = self.is_hand_idle and not self.is_recent_dance
        self.was_ready = self.count_ready_valid > 0
        self.is_turn_cooldown = self.count_turn_lockout > 0
        self.is_anti_shake = self.count_above_left_threshold_timout>0 and self.count_above_right_threshold_timout>0
        self.is_small_move = self.count_move_total_duration < MINIMUM_LARGE_MOVE_TIME
        self.is_hand_high = abs(aZ_norm + (GRAVITY_Z) ) < FINISHER_GRAVITY_THRESHOLD


        # ====Per sample Cooldowns====
        if self.count_above_left_threshold_timout>0:
            self.count_above_left_threshold_timout-=1
        if self.count_above_right_threshold_timout>0:
            self.count_above_right_threshold_timout-=1

        if self.is_hand_high:
            self.count_consecutive_hand_high +=1
        else:
            self.count_consecutive_hand_high =0


        if self.is_turn_cooldown:
            self.count_turn_lockout -=1
        else:
            self.count_turn_lockout = 0
        
        if self.was_ready:
            self.count_ready_valid -= 1

        if self.is_ready:
            self.count_ready_valid = READY_VALIDITY_SAMPLES
        
        # ===updating internal state machine===
        if self.is_dancing:
            # If dancing, must not be ready
            self.is_ready =False
            self.count_ready_valid = 0 
            # If dancing, reduce move_end_coundown
            self.count_move_timeout -= 1
            # Increment dance time counter
            self.count_move_total_duration +=1

            if (self.count_consecutive_hand_high > FINISHER_MOVE_MIN_SAMPLES and _IS_MAIN and self.is_current_move_valid):
               self.stopPrediction(logout=True)
               self.is_current_move_valid = False

            if (self.count_move_total_duration > PREDICTION_SAMPLES) and USE_PREDICTION_SAMPLES and self.is_current_move_valid:
                self.stopPrediction()
                self.is_current_move_valid = False

            if (not self.is_hand_returned_to_idle) or self.is_large_movement:
                # If Big movement is detected or hand is not in Idle Position, 
                # Remain dancing and reset move timeouit
                self.is_dancing = True
                if not self.is_current_move_valid:
                    self.count_move_timeout = MOVE_TIMEOUT_MAX_MEDIUM
                elif self.is_small_move:
                    self.count_move_timeout = MOVE_TIMEOUT_MAX_SHORT
                else:
                    self.count_move_timeout = MOVE_TIMEOUT_MAX_LONG


            elif self.count_move_timeout < 0:
                # if move times out, consider move ended
                print("{} MoveTimout".format(self.deviceName))
                self.is_dancing = False
            
            # if dance ends, report and run prediction
            if not self.is_dancing:
                # print("Device {} Dance Move Ended. {} Samples".format(
                #     self.deviceName,
                #     self.count_move_total_duration
                #     ))
                if self.is_current_move_valid:
                    self.stopPrediction()
    
                # reset Move sample count
                self.count_move_total_duration = 0

        elif not self.is_dancing:
            # if Ready and large movement
            if (self.is_ready or self.was_ready) and self.is_large_movement:
                self.count_consecutive_high_energy+=1
                if self.count_consecutive_high_energy > CONSEC_HIGH_DANCE_THRESH:
                    print("{} activation | G:{} | zG:{}".format(self.deviceName,aMag-GRAVITY_TRUE_MAG,aZ_norm - (GRAVITY_Z)))
                    
                    self.is_dancing = True
                    self.is_current_move_valid = True
                    self.count_move_timeout = MOVE_TIMEOUT_MAX_SHORT
                    self.startPrediction()
            else:
                self.count_consecutive_high_energy = 0 

        
        # rotation detection
        if (not self.is_dancing) and self.is_hand_idle and not self.is_turn_cooldown and not self.is_anti_shake:
            if gZ_norm > RIGHT_TURN_THRESH and gZ_norm > 0 :
                self.count_above_right_threshold_timout = ANTI_SHAKE_COOLDOWN
                self.count_consecutive_high_turns += 1
                if self.count_consecutive_high_turns > CONSEC_HIGH_TURN_THRESH:
                    self.is_turn_cooldown = True
                    self.count_turn_lockout = TURN_LOCKOUT_SAMPLES
                    # print("Dev: {} Right Turn".format(self.deviceName))
                    self.pushTurnEvent("right")
            elif gZ_norm < LEFT_TURN_THRESH and gZ_norm < 0 :
                self.count_above_left_threshold_timout = ANTI_SHAKE_COOLDOWN
                self.count_consecutive_high_turns += 1
                if self.count_consecutive_high_turns > CONSEC_HIGH_TURN_THRESH:
                    self.is_turn_cooldown = True
                    self.count_turn_lockout = TURN_LOCKOUT_SAMPLES
                    # print("Dev: {} Left Turn".format(self.deviceName))
                    self.pushTurnEvent("left")
            else:
                self.count_consecutive_high_turns =0



         
        # Updating Internal Buffers
        currentActivationState = self.calculateActivation()
        self.updateInternalBuffers(aX_norm,aY_norm,aZ_norm,gX_norm,gY_norm,gZ_norm,currentActivationState)
        
        # Updating Submodules and Comms
        self.updatePredictor()
        self.updateRecorder()
        self.sendSample()

    def updateInternalBuffers(self, aX,aY,aZ,gX,gY,gZ,activityState):
        self.pushToBuffer(self.aX, aX)
        self.pushToBuffer(self.aY, aY)
        self.pushToBuffer(self.aZ, aZ)
        self.pushToBuffer(self.gX, gX)
        self.pushToBuffer(self.gY, gY)
        self.pushToBuffer(self.gZ, gZ)
        self.pushToBuffer(self.actList, activityState)

    def updateWatchdog(self):
        if self.is_connected:
            self.count_connection_timeout -=1
            if self.count_connection_timeout <= 0:
                print("Device {} disconnected!".format(self.deviceName))
                self.is_connected = False

    def pushTurnEvent(self, turnDir):
        if not self.turnEventCallback == None and IS_IN_PASSTHROUGH_MODE == False:
            self.turnEventCallback(self.deviceName,turnDir )

    # =======HELPER CALCULATION FUNCTIONS========
    def calculateMovingAverage(self, aX,aY,aZ,gX,gY,gZ):
        aX = aX*NEWWEIGHT + self.aX[-1]*OLDWEIGHT
        aY = aY*NEWWEIGHT + self.aY[-1]*OLDWEIGHT
        aZ = aZ*NEWWEIGHT + self.aZ[-1]*OLDWEIGHT
        return (aX,aY,aZ)

    def calculateAccelMagnitude(self,acceleration_x,acceleration_y,acceleration_z ):       
        return (acceleration_x**2 +acceleration_y**2 +acceleration_z**2)**(0.5)
    
    def calculateNormalizedAcceleration(self,aX,aY,aZ):
        return list(map(lambda x: int(x)/64,[aX,aY,aZ]))

    def calculateNormalizedGyroscope(self,gX,gY,gZ):
        return list(map(lambda x: (int(x)/128 * 250) ,[gX,gY,gZ]))


    def calculateActivation(self):
        updateValue = 0
        if self.is_ready:
            updateValue = 1
        if self.is_dancing:
            updateValue = 2
        return updateValue

    def pushToBuffer(self, buffer, value):
        buffer.pop(0)
        buffer.append(value)

    # ======== PREDICTION FUNCTIONS ===========
    def startPrediction(self):
        if not self.predictor == None and IS_IN_PASSTHROUGH_MODE == False:
            self.predictor.startRecording()
    def stopPrediction(self, logout =False):
        if not self.predictor == None and IS_IN_PASSTHROUGH_MODE == False:
            if logout:
                result = ["logout"]
                self.predictor.clearInternalBuffers()
                print("=========DETECTED LOGOUT===========")
            else:
                result = self.predictor.stopRecording()
            if not result == None:
                self.predictionEventCallback(self.deviceName,result[0])
    def updatePredictor(self):
        if not self.predictor == None and IS_IN_PASSTHROUGH_MODE == False:
            self.predictor.update()

    def cancelPrediction(self):
        if not self.predictor == None and IS_IN_PASSTHROUGH_MODE == False:
            self.predictor.cancel()
    def setPostDanceState(self):
        self.is_current_move_valid = False
    # ======== Relay Specific Functions ========

    def toggleSendFlag(self):
        self.transmitToUltra = not self.transmitToUltra

    def updateRecorder(self):
        if not self.recordingModule == None:
            self.recordingModule.update()
    
    def getRecorder(self):
        return self.recordingModule
            
    def sendSample(self):
        if self.connectionToUltra and (not self.isUltra96) and self.transmitToUltra:
            a_x = self.aX[-1]
            a_y = self.aY[-1]
            a_z = self.aZ[-1]

            g_x = self.gX[-1]
            g_y = self.gY[-1]
            g_z = self.gZ[-1]
            # message = "!D|" + f"{addr_map[self.addr]}" + "|" + "|".join(data[1].split(",")) + "|"
            msg = "!D|{id}|{a_x}|{a_y}|{a_z}|{g_x}|{g_y}|{g_z}|{ts}|".format(
                id = self.DEV_NAME_TO_EXT_COMMS_ID[self.deviceName] ,
                a_x = a_x,
                a_y = a_y,
                a_z = a_z,
                g_x = g_x,
                g_y = g_y,
                g_z = g_z,
                ts = int(round(time.time() * 10000))
            )
            self.connectionToUltra.send_message(msg)

class DeviceDataBufferMyoWare():
    def __init__(self,deviceName, isRunningOnUltra = False, connectionToUltra = None):
        # declaration of internal state/attributes
        self.deviceName = deviceName
        self.isUltra96 = isRunningOnUltra
        self.connectionToUltra = connectionToUltra
        self.transmitToUltra = False
        
        # Internal buffers 
        self.RMSList = [0] * DATA_BUFFER_INTERNAL_BUFFER_SIZE 
        self.MAVList = [0] * DATA_BUFFER_INTERNAL_BUFFER_SIZE 
        self.ZCSList = [0] * DATA_BUFFER_INTERNAL_BUFFER_SIZE 
    
    def toggleSendFlag(self):
        self.transmitToUltra = not self.transmitToUltra
        
    def updateInternalState(self,R,M,Z):
        self.RMSList.pop(0)
        self.MAVList.pop(0)
        self.ZCSList.pop(0) 
        self.RMSList.append(R)
        self.MAVList.append(M)
        self.ZCSList.append(Z)

        self.sendSample()

        # print(R,M,Z)

    def sendSample(self):
        if self.connectionToUltra and (not self.isUltra96) and self.transmitToUltra:
            rms = self.RMSList[-1]
            mav = self.MAVList[-1]
            zcs = self.ZCSList[-1]
            # print('test')

            # message = "!D|" + f"{addr_map[self.addr]}" + "|" + "|".join(data[1].split(",")) + "|"
            msg = "!E|{id}|{rms}|{mav}|{zcs}|{ts}|".format(
                id = 1,
                rms = rms,
                mav = mav,
                zcs = zcs,
                ts = int(round(time.time() * 10000))
            )
            self.connectionToUltra.send_message(msg)

# This class stores and records data from a device.
# This class is meant to be initialized within datadeviceBuffer
class DataRecorder():
    def __init__(self, parentBuffer):
        # declaration of internal state/attributes
        self.parent = parentBuffer
        self.currentMove = "defaultMove"
        self.is_Recording = False
        # ===Data===
        self.aX = []
        self.aY = []
        self.aZ = []
        self.gX = []
        self.gY = []
        self.gZ = []

        self.actList = []

        # self.data_list = [aX,aY,aZ,gX,gY,gZ,actList]

        # ===counters===
        self.count_move_total_duration = 0

    # ========STATE MANAGEMENT FUNCTIONS==========
    def clearInternalBuffers(self):
        self.aX = []
        self.aY = []
        self.aZ = []
        self.gX = []
        self.gY = []
        self.gZ = []
        self.actList = []
        self.count_move_total_duration = 0

    def update(self):
        databuffer = self.parent
        if self.is_Recording:
            self.count_move_total_duration +=1
            self.aX.append(databuffer.aX[-1])
            self.aY.append(databuffer.aY[-1])
            self.aZ.append(databuffer.aZ[-1])
            self.gX.append(databuffer.gX[-1])
            self.gY.append(databuffer.gY[-1])
            self.gZ.append(databuffer.gZ[-1])
            self.actList.append(databuffer.actList[-1])
    
    def startRecording(self):
        print("Recording Started For {} on {}".format(self.parent.deviceName, self.currentMove))
        self.is_Recording = True
    
    def stopRecording(self):
        if self.count_move_total_duration == 0:
            print("Recording Cancelled For {} on {}".format(self.parent.deviceName, self.currentMove))
            return None
        self.saveRecording()
        self.is_Recording = False
        self.clearInternalBuffers()
    
    def saveRecording(self):
        timeNow = round(time.time() * 10000)
        fName = self.parent.deviceName + "_" + self.currentMove + "_" + str(timeNow)
        savePath = os.path.join(BASEPATH,SAVE_FOLDER_NAME_DATARECORDER, fName)
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
            for idx in range(len(self.aX)):
                row = [
                    self.aX[idx],
                    self.aY[idx],
                    self.aZ[idx],
                    self.gX[idx],
                    self.gY[idx],
                    self.gZ[idx],
                    self.actList[idx]
                ] 
                csvWriter.writerow(row)
            print("Recording saved as {}. Saved {} samples".format(fName, self.count_move_total_duration))
    
class positionTrackingSystem():
    DEVICE_NAME_TO_INDEX = {
        "dev1" : 0, 
        "dev2" : 1, 
        "dev3" : 2
    }
    DEVICE_INDEX_TO_NAME = {
        0:"dev1",
        1:"dev2",
        2:"dev3"
    }
    TRANSLATION_MATRIX = {
        ('left', 'left', 'right') : ( 2, 0, 1),
        ('left', 'right', 'right') : ( 1, 2, 0),
        ('left', 'still', 'right') : ( 2, 1, 0),
        ('left', 'right', 'still') : ( 1, 0, 2),
        ('still', 'left', 'right') : ( 0, 2, 1),
        ('still', 'still', 'still') : ( 0, 1 ,2)
    }
    def __init__(self):
        self.turnDevices = ["still","still","still"]
        self.posDevices = [0,1,2][::-1]
        self.is_already_turned = [False,False,False]
        self.is_position_valid = False
        self.count_validity = -1

        pass
    
    def update(self):
        if self.count_validity > 0:
            self.count_validity-=1
            # print(self.count_validity)
        if self.count_validity == 0 and not self.is_position_valid:
            # self.calculateNewPosition(self.posDevices)
            print("POS INVALIDATED. | {} | {} | {} | {}". format(
                self.turnDevices,
                self.is_already_turned,
                self.posDevices,
                self.is_position_valid,
            ))
            self.invalidateAndReset()
    
    def pushTurnEvent(self, deviceName, turnDirection):
        devID = self.DEVICE_NAME_TO_INDEX[deviceName]
        self.count_validity = TURN_VALIDITY_MAX_SAMPLES
        if not self.is_already_turned[devID]:
            self.turnDevices[devID] = turnDirection
            self.is_already_turned[devID] = True
            print("{} TURN {} | {} | {} | {} | {}". format(
                deviceName,
                turnDirection,
                self.turnDevices,
                self.is_already_turned,
                self.posDevices,
                self.is_position_valid,
            ))

            if not (False in self.is_already_turned):
                newPos = self.calculateNewPosition(self.posDevices)
                if not newPos == None:
                    self.posDevices =newPos
                    self.is_position_valid = True

    def calculateNewPosition(self, oldPos):
        arragementInPositionOrder = [None,None,None]
        turnsInPositionOrder = ["still","still","still"]

        for idx,pos in enumerate(self.posDevices):
            # device id == idx
            arragementInPositionOrder[idx] = self.DEVICE_INDEX_TO_NAME[pos]
            turnsInPositionOrder[idx] = self.turnDevices[pos]

        translationVector = self.TRANSLATION_MATRIX.get(tuple(turnsInPositionOrder), None)

        if translationVector == None:
            # print("POS FAIL | {} is invalid for {}".format(turnsInPositionOrder, self.posDevices))
            turnStr = """
                ===========CALCULATE TURNS=============
                CurrentPosition = {}
                TurnVector = {}
                NewPosition = {}
                ===========END=============
                """.format(list(map(lambda x: x+1 , self.posDevices)),self.turnDevices,"FAIL")
            print(turnStr)
            return None

        newPositions= [None,None,None]
        for idx,idAtPos in enumerate(translationVector):
            newPositions[idx] = arragementInPositionOrder[idAtPos]
        newPositions = list(map(lambda x: self.DEVICE_NAME_TO_INDEX[x],newPositions ))
        # print("NEW POS CALC | Old Position: {} | NewPosition {}".format(
        #     self.posDevices,
        #     newPositions
        # ))
        turnStr = """
            ===========CALCULATE TURNS=============
            CurrentPosition = {}
            TurnVector = {}
            NewPosition = {}
            ===========END=============
            """.format(list(map(lambda x: x+1 , self.posDevices)),self.turnDevices,list(map(lambda x: x+1 , newPositions)))
        print(turnStr)
        return newPositions




    def invalidateAndReset(self, set_position = None):
        if not set_position == None:
            set_position = set_position[::-1]
            self.posDevices = set_position

        self.turnDevices = ["still","still","still"]
        self.is_already_turned  = [False,False,False]
        self.is_position_valid = False
        self.count_validity = -1

    def readAndInvalidate(self):
        if self.is_position_valid:
            res = self.posDevices
            self.invalidateAndReset()
            return res
        else:
            newPos = self.calculateNewPosition(self.posDevices)
            if not newPos == None:
                self.posDevices = newPos
            else:
                newPos = self.posDevices
            self.invalidateAndReset()
            return newPos
    
    def getState(self):
        return [self.turnDevices,self.posDevices,self.is_already_turned,self.is_position_valid,self.count_validity]

class predictionEnsembleManager():
    DEVICE_NAME_TO_INDEX = {
        "dev1" : 0, 
        "dev2" : 1, 
        "dev3" : 2
    }
    DEVICE_INDEX_TO_NAME = {
        0:"dev1",
        1:"dev2",
        2:"dev3"
    }
    
    def __init__(self,ULTRAcallback,readOrientation):
        self.readOrientation = readOrientation
        self.ULTRAcallback = ULTRAcallback

        self.predictions = [None,None,None]
        self.predictions_lag_samples_count = [0,0,0]
        self.is_already_predicted= [False,False,False]
        self.count_validity = -1


        pass

    def update(self):
        if self.count_validity > 0:
            self.count_validity-=1
        if self.count_validity == 0:
            # self.submitPrediction()
            print("PRED RESET | {} | {} | {}".format(self.predictions,self.is_already_predicted,self.predictions_lag_samples_count))
            self.reset()

        if self.count_validity > 0 :
            for i in range(3):
                if self.is_already_predicted[i] == False:
                    self.predictions_lag_samples_count[i] += 1

    def pushPredictionEvent(self, deviceName, predictionResult):
        devID = self.DEVICE_NAME_TO_INDEX[deviceName]
        if not self.is_already_predicted[devID]:
            self.is_already_predicted[devID] =True
            self.predictions[devID] = predictionResult
            self.count_validity =  PREDICTION_ENSEMBLE_MAX_COUNT_VALID

        if not (False in self.is_already_predicted) or SOLO_TEST_MODE:
            self.submitPrediction()

    def reset(self):
        self.predictions = [None,None,None]
        self.is_already_predicted= [False,False,False]
        self.predictions_lag_samples_count = [0,0,0]
        self.count_validity = -1

    def submitPrediction(self):
        occurence_count = libCounter(self.predictions)
        most_common = occurence_count.most_common()
        ordered = list(filter(lambda x: not x[0] == None, most_common ))
        # TODO: add client Code here
        orientation = self.readOrientation()
        predictedResult = ordered[0][0]
        syncDelay = self.predictions_lag_samples_count

        print("===================")
        print("Predictions {} | Final Prediction: {} | Lag Vector {} ".format(self.predictions , ordered,  ordered[0][0]))
        print("Lag Vector {} | Final Pos {}".format(self.predictions_lag_samples_count,orientation))
        print("===================")
        self.ULTRAcallback(orientation, predictedResult, syncDelay)
        self.reset()

    def getState(self):
        return [self.predictions,self.predictions_lag_samples_count,self.is_already_predicted,self.count_validity]


if not IS_RUNNING_ON_ULTRA:
    import matplotlib.pyplot as plt
    from matplotlib.widgets import TextBox, Button, RadioButtons
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import gridspec

# This class handles the display for all the devices
class liveDataDisplay():
    def __init__(self, d1,d2,d3, myowareBuffer):
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.buffers = [d1,d2,d3]
        self.myowareBuffer = myowareBuffer
        self.is_kill_signal = False

        self.uiThread = Thread(target=self.displayThreadTarget)
        self.uiThread.daemon = True

    def recordButtonCallbackGenerator(self,list_of_data_collectors):
        def callback(e):
            for dc in list_of_data_collectors:
                dc.startRecording()
        return callback

    def stopButtonCallbackGenerator(self,list_of_data_collectors):
        def callback(e):
            for dc in list_of_data_collectors:
                dc.stopRecording()
        return callback

    def toggleSendDataCallbackGenerator(self,list_of_data_collectors):
        def callback(e):
            for dc in list_of_data_collectors:
                dc.toggleSendFlag()
        return callback

    def radioBoxSubmitCallbackGenerator(self,list_of_data_collectors):
        def callback(text):
            for dc in list_of_data_collectors:
                dc.currentMove = text
        return callback

    def configurePlots(self,index,accel,gyro,activation,deviceData,deviceID):
        activation.set_title("Device " + str(deviceID) + "\nActivation" )
        accel.set_title("Accel" )
        gyro.set_title("Gyro" )

        # TODO plot the activation

        ax1, = accel.plot(index, deviceData.aX, label = "X")
        ax2, = accel.plot(index, deviceData.aY, label = "Y")
        ax3, = accel.plot(index, deviceData.aZ, label = "Z")

        ax4, = gyro.plot(index, deviceData.gX, label = "X")
        ax5, = gyro.plot(index, deviceData.gY, label = "Y")
        ax6, = gyro.plot(index, deviceData.gZ, label = "Z")

        ax7, = activation.plot(index, deviceData.actList, label = "R")
        

        activation.set_xlim(xmin = 0 , xmax = DATA_BUFFER_INTERNAL_BUFFER_SIZE )
        activation.set_ylim(ymin = 0.2 , ymax = 2.2 )

        accel.set_xlim(xmin = 0 , xmax = DATA_BUFFER_INTERNAL_BUFFER_SIZE )
        accel.set_ylim(ymin = -2 , ymax = 2 )

        gyro.set_xlim(xmin = 0 , xmax = DATA_BUFFER_INTERNAL_BUFFER_SIZE )
        gyro.set_ylim(ymin = -250 , ymax = 250 )

        if deviceID == 1:
            accel.legend((ax1, ax2, ax3), ('X', 'Y', 'Z'), loc ='upper right', bbox_to_anchor=(0, 1),fontsize='xx-small' )
            gyro.legend((ax4, ax5, ax6), ('X', 'Y', 'Z'), loc ='upper right', bbox_to_anchor=(0, 1),fontsize='xx-small')

        return [ax1,ax2,ax3,ax4,ax5,ax6,ax7]

    def configureMyowarePlot(self,index,rms,mav,zcr,deviceData):
        ax1, = rms.plot(index, deviceData.RMSList, label = "rms")
        ax2, = mav.plot(index, deviceData.MAVList, label = "mav")
        ax3, = zcr.plot(index, deviceData.ZCSList, label = "zcr")

        rms.set_title("rms" )
        mav.set_title("mav" )
        zcr.set_title("zcr" )

        rms.set_xlim(xmin = 0 , xmax = DATA_BUFFER_INTERNAL_BUFFER_SIZE )
        rms.set_ylim(ymin = 0 , ymax = 255 )

        mav.set_xlim(xmin = 0 , xmax = DATA_BUFFER_INTERNAL_BUFFER_SIZE )
        mav.set_ylim(ymin = 0 , ymax = 255 )

        zcr.set_xlim(xmin = 0 , xmax = DATA_BUFFER_INTERNAL_BUFFER_SIZE )
        zcr.set_ylim(ymin = 0 , ymax = 255 )
        return [ax1,ax2,ax3]

    def updatePlotData(self,index,plotAxis,deviceData):
        ax1,ax2,ax3,ax4,ax5,ax6, ax7 = plotAxis
        ax1.set_data(index, deviceData.aX)
        ax2.set_data(index, deviceData.aY)
        ax3.set_data(index, deviceData.aZ)

        ax4.set_data(index, deviceData.gX)
        ax5.set_data(index, deviceData.gY)
        ax6.set_data(index, deviceData.gZ)

        ax7.set_data(index, deviceData.actList)

    def updatePlotDataMyoware(self,index,plotAxis,deviceData):
        ax1,ax2,ax3 = plotAxis
        ax1.set_data(index, deviceData.RMSList)
        ax2.set_data(index, deviceData.MAVList)
        ax3.set_data(index, deviceData.ZCSList)
        
    def displayThreadTarget(self):
        index = []
        for i in range(DATA_BUFFER_INTERNAL_BUFFER_SIZE):
            index.append(i)
        try:
            fig2 = plt.figure(1)
            gs = gridspec.GridSpec(3, 5, width_ratios=[1,1,1,1,1], height_ratios=[0.2,1,1]) 

            axRecord = fig2.add_axes([0.7, 0.02, 0.1, 0.075])
            axStop = fig2.add_axes([0.81, 0.02, 0.1, 0.075])
            axText = fig2.add_axes([0.01, 0.02, 0.1, 0.2])
            axTransmit = fig2.add_axes([0.81, 0.22, 0.1, 0.075])



            listDC = list(map(lambda x: x.getRecorder(),self.buffers))
            bRecord = Button(axRecord, 'Record')
            bRecord.on_clicked(self.recordButtonCallbackGenerator(listDC))
            bStop = Button(axStop, 'Stop')
            bStop.on_clicked(self.stopButtonCallbackGenerator(listDC))
            radioB= RadioButtons(axText, DANCEMOVENAMES)
            radioB.on_clicked(self.radioBoxSubmitCallbackGenerator(listDC))

            btransmit = Button(axTransmit, 'ToggleTransmit')
            btransmit.on_clicked(self.toggleSendDataCallbackGenerator(self.buffers + [self.myowareBuffer]))

            DEV1_activation = fig2.add_subplot(gs[0,0])
            DEV2_activation  = fig2.add_subplot(gs[0,1])
            DEV3_activation  = fig2.add_subplot(gs[0,2])

            DEV1_accel = fig2.add_subplot(gs[1,0])
            DEV2_accel = fig2.add_subplot(gs[1,1])
            DEV3_accel = fig2.add_subplot(gs[1,2])

            DEV1_gyro = fig2.add_subplot(gs[2,0])
            DEV2_gyro = fig2.add_subplot(gs[2,1])
            DEV3_gyro = fig2.add_subplot(gs[2,2]) 

            myoware_rms = fig2.add_subplot(gs[1,4])
            myoware_mav = fig2.add_subplot(gs[1,3])
            myoware_zcr = fig2.add_subplot(gs[2,3]) 

            DEV1_AXIS = self.configurePlots(index,DEV1_accel,DEV1_gyro,DEV1_activation,self.d1,1)
            DEV2_AXIS = self.configurePlots(index,DEV2_accel,DEV2_gyro,DEV2_activation,self.d2,2)
            DEV3_AXIS = self.configurePlots(index,DEV3_accel,DEV3_gyro,DEV3_activation,self.d3,3)
            MYOWARE_AXIS = self.configureMyowarePlot(index,myoware_rms,myoware_mav,myoware_zcr,self.myowareBuffer)


            plt.ion()
            plt.pause(1)
            plt.show()
            while(not _IS_KILL):
                self.updatePlotData(index,DEV1_AXIS,self.d1)
                self.updatePlotData(index,DEV2_AXIS,self.d2)
                self.updatePlotData(index,DEV3_AXIS,self.d3)
                self.updatePlotDataMyoware(index,MYOWARE_AXIS, self.myowareBuffer)
                plt.pause(0.25)
            plt.close('all')
            print("Gracefull Exit")

        except Exception as a:
            traceback.print_exc()
            print("exiting")
            return

    def startThread(self):
        self.uiThread.start()

# This class buffers prediction Data
class predictorBuffer():
    def __init__(self, parentBuffer, predictionEngine):
        self.predictionEngine = predictionEngine
        self.parent = parentBuffer
        self.is_Move = False
        self.is_cancelled=False
        # ===Data===
        self.aX = []
        self.aY = []
        self.aZ = []
        self.gX = []
        self.gY = []
        self.gZ = []
        self.actList = []
        self.count_move_total_duration = 0

    def clearInternalBuffers(self):
        self.aX = []
        self.aY = []
        self.aZ = []
        self.gX = []
        self.gY = []
        self.gZ = []
        self.actList = []
        self.count_move_total_duration = 0
        self.is_cancelled =False
        self.is_Move = False

    def startRecording( self ):
        self.is_Move = True

    def stopRecording( self ):
        if self.is_cancelled:
            print("{} PRED: CANCELLED".format(self.parent.deviceName))
            self.is_cancelled = False
            self.is_Move = False
            self.clearInternalBuffers()
            return None 
        
        if self.count_move_total_duration < MIN_MOVE_TIME_SAMPLES :
            print("{} Too Short!".format(self.parent.deviceName))
            self.is_Move = False
            self.count_move_total_duration = 0
            self.clearInternalBuffers()
            return None
        else:
            # print("Move Ended. Predicting")
            res = self.predict()
            print("{} PRED: {} | {}".format(self.parent.deviceName,res[0] ,self.count_move_total_duration))
            self.is_Move = False
            self.count_move_total_duration = 0
            self.clearInternalBuffers()
            return res

    def cancel(self):
        if self.is_Move:
            self.is_cancelled = True

    def update(self):
        if self.is_Move:
            if (self.count_move_total_duration == 0):
                self.count_move_total_duration +=1
                self.aX.extend(self.parent.aX[-PREDICTION_PRE_SAMPLES:])
                self.aY.extend(self.parent.aY[-PREDICTION_PRE_SAMPLES:])
                self.aZ.extend(self.parent.aZ[-PREDICTION_PRE_SAMPLES:])
                self.gX.extend(self.parent.gX[-PREDICTION_PRE_SAMPLES:])
                self.gY.extend(self.parent.gY[-PREDICTION_PRE_SAMPLES:])
                self.gZ.extend(self.parent.gZ[-PREDICTION_PRE_SAMPLES:])         
                self.actList.extend(self.parent.actList[-PREDICTION_PRE_SAMPLES:])
            else:
                self.count_move_total_duration +=1
                self.aX.append(self.parent.aX[-1])
                self.aY.append(self.parent.aY[-1])
                self.aZ.append(self.parent.aZ[-1])
                self.gX.append(self.parent.gX[-1])
                self.gY.append(self.parent.gY[-1])
                self.gZ.append(self.parent.gZ[-1])         
                self.actList.append(self.parent.actList[-1])

    def padData(self,data,padlength):
        pad =  [data[-1]] * padlength
        data.extend(pad)

    def preparePrediction(self, offset = PREDICTION_PRE_SAMPLES):

        a_xList = self.aX[offset:MAX_SAMPLES + offset]
        a_yList = self.aY[offset:MAX_SAMPLES + offset]
        a_zList = self.aZ[offset:MAX_SAMPLES + offset]
        g_xList = self.gX[offset:MAX_SAMPLES + offset]
        g_yList = self.gY[offset:MAX_SAMPLES + offset]
        g_zList = self.gZ[offset:MAX_SAMPLES + offset]
        activation_List = self.actList[:MAX_SAMPLES + offset]

        if len(a_xList) < MAX_SAMPLES:
            padLength = MAX_SAMPLES - len(a_xList)
            # print("padded {} samples with {}.".format(len(a_xList) , padLength))
            self.padData(a_xList,padLength)
            self.padData(a_yList,padLength)
            self.padData(a_zList,padLength)
            self.padData(g_xList,padLength)
            self.padData(g_yList,padLength)
            self.padData(g_zList,padLength)
            self.padData(activation_List,padLength)

  
        return [
            a_xList,
            a_yList,
            a_zList,
            g_xList,
            g_yList,
            g_zList,
            activation_List
        ]

    def predict(self, single = False):
        if single:
            res = []
            for i in range(0, PREDICTION_PRE_SAMPLES + 11 , 2):
                d = self.preparePrediction(offset=i)
                res.append(self.predictionEngine.predict(self.parent.deviceName,d))
            print("ensemble Result:" ,res )
            return res
        else:
            d = self.preparePrediction(offset=PREDICTION_PRE_SAMPLES)
            res = [self.predictionEngine.predict(self.parent.deviceName,d)]
            return res


# This class buffers prediction Data
class ExternalConnectionInterface():
    def __init__(self):
        pass

# Top Class, Manages everything
class liveDataEngine():
    def __init__(self,isRunningOnUltra = False, connectionToUltra = None , initDataRecording = False, predictor = None, UlTRACallback =None):

        self.UlTRACallback = UlTRACallback
        self.positionTracker = positionTrackingSystem()
        self.predictionEnsembleEngine = predictionEnsembleManager(self.runULTRAcallback , self.positionTracker.readAndInvalidate)
        

        self.device_1 = DeviceDataBuffer(
            "dev1",
            isRunningOnUltra = isRunningOnUltra, 
            connectionToUltra = connectionToUltra, 
            initDataRecording = initDataRecording, 
            predictor = predictor,
            turnEventCallback = self.positionTracker.pushTurnEvent,
            predictionEventCallback = self.predictionEnsembleEngine.pushPredictionEvent
            )

        self.device_2 = DeviceDataBuffer(
            "dev2",
            isRunningOnUltra = isRunningOnUltra, 
            connectionToUltra = connectionToUltra, 
            initDataRecording = initDataRecording, 
            predictor = predictor,
            turnEventCallback = self.positionTracker.pushTurnEvent,
            predictionEventCallback = self.predictionEnsembleEngine.pushPredictionEvent
            )

        self.device_3 = DeviceDataBuffer(
            "dev3",
            isRunningOnUltra = isRunningOnUltra, 
            connectionToUltra = connectionToUltra, 
            initDataRecording = initDataRecording, 
            predictor = predictor,
            turnEventCallback = self.positionTracker.pushTurnEvent,
            predictionEventCallback = self.predictionEnsembleEngine.pushPredictionEvent
            )

        self.device_MyoWare = DeviceDataBufferMyoWare(
            "dev1",
            isRunningOnUltra = isRunningOnUltra, 
            connectionToUltra = connectionToUltra
            )
        
        self.deviceList = [self.device_1,self.device_2,self.device_3]
        self.masterDevice = None



        if not isRunningOnUltra:
            self.displayEngine = liveDataDisplay(
                self.device_1,
                self.device_2,
                self.device_3,
                self.device_MyoWare
                )
        else:
            self.displayEngine = None
    def start(self):
        if not self.displayEngine == None:
            self.displayEngine.startThread()

    def updateDeviceWatchdog(self):
        for device in self.deviceList:
            device.updateWatchdog()
    
    def updateMasterDevice(self):
        for device in self.deviceList:
            if device.is_connected:
                self.masterDevice = device
                return device
        self.masterDevice = None
        return None

    def updateSystemwideTasks(self,devID):
        if self.deviceList[devID-1] is self.masterDevice:
            # TODO: Run system wide updates
            self.positionTracker.update()
            self.predictionEnsembleEngine.update()
            pass

    def updatePlots(self,devID, aX,aY,aZ, gX,gY,gZ):
        if not devID == 'Myo':
            # updates watchdog functions for all devices
            self.updateDeviceWatchdog()
            # updates current master device
            self.updateMasterDevice()
            self.updateSystemwideTasks(devID)

        if devID == 'Myo':
            self.device_MyoWare.updateInternalState(aX,aY,aZ)
        else:
            self.deviceList[devID-1].updateInternalState(aX,aY,aZ, gX,gY,gZ)

    def runULTRAcallback(self, position , predictedResult, syncDelay):
        SAMPLINGPERIOD = 50
        if self.UlTRACallback == None:
            print("DID NOT RUN")
            return
        else:
            position = position[::-1]
            formattedPos = "#{} {} {}".format(position[0]+1, position[1]+1, position[2]+1)
            formattedSyncDelay= "{} {} {}".format(syncDelay[0] * SAMPLINGPERIOD , syncDelay[1] * SAMPLINGPERIOD, syncDelay[2] * SAMPLINGPERIOD)
            formattedPredictionResult = predictedResult

            evalSyncmax = (self.getSyncDelayFromList(syncDelay) * SAMPLINGPERIOD )/1000

            if evalSyncmax>MAX_SYNC:
                evalSyncmax = float(MAX_SYNC)
            formattedEVALSyncDelay = str(evalSyncmax)


            dashFormattedSyncDelay = "{} {} {}".format(syncDelay[0]* SAMPLINGPERIOD, syncDelay[1] * SAMPLINGPERIOD, syncDelay[2] * SAMPLINGPERIOD )
            self.UlTRACallback(formattedPos,predictedResult,dashFormattedSyncDelay,formattedEVALSyncDelay)
        # ULTRAcallback(orientation, predictedResult, syncDelay)

    def getSyncDelayFromList(self, syncList):
        startTime = min(syncList)
        stopTime = max(syncList)
        return stopTime-startTime

    def cancelOngoingPredictions(self):
        for dev in self.deviceList:
            dev.cancelPrediction()

    def evalServerReplySet(self, pos):
        self.positionTracker.invalidateAndReset(set_position= pos)
        for dev in self.deviceList:
            dev.setPostDanceState()
        self.predictionEnsembleEngine.reset()

        print("=====================\nEVAL RESET! | newPos {}\n{}\n=====================".format(pos,self.predictionEnsembleEngine.getState(),self.positionTracker.getState()))




# TODO: put ultra connection here
if IS_CONNECT_TO_ULTRA and not IS_RUNNING_ON_ULTRA:
    print("HELOOOOO")
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(CURRENT_DIR))
    from external_comms.laptop_client import Client
    # client to connect to fpga
    HOST_ADDR = ('localhost', 8081)
    EN_FORMAT = "utf-8"
    DANCER_NAME = "XY"
    SECRET_KEY = "9999999999999999"
    BUFF_SIZE = 256
    ULTRA_CONN = Client(HOST_ADDR, EN_FORMAT, 1, SECRET_KEY, DANCER_NAME, BUFF_SIZE)

else:
    ULTRA_CONN = None

# Conditional import for the prediction engine

if IS_RUNNING_ON_ULTRA and IS_PREDICTOR :
    # TODO: write the ultra predictor
    # from ultraPredictor import Predictor
    from Test.relayPredictor_ultra96 import Predictor as Predictor
    PREDICTOR = Predictor()
elif (not IS_RUNNING_ON_ULTRA) and IS_PREDICTOR:
    from relayPredictor import Predictor as Predictor
    PREDICTOR = Predictor()
else:
    PREDICTOR = None
    

ENGINE = liveDataEngine(
    isRunningOnUltra = IS_RUNNING_ON_ULTRA, 
    connectionToUltra = ULTRA_CONN , 
    initDataRecording = IS_DATA_RECORDER,
    predictor = PREDICTOR,
    UlTRACallback=None
    )


if not IS_RUNNING_ON_ULTRA:
    # ========BLE SERVER CODE===========
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
                while(len(buf) > myowareDecode.size + headerDecode.size ):
                    # ts, depthsize ,rbgsize = tsDecode.unpack(buf[:tsDecode.size])
                    DeviceID, packetType = headerDecode.unpack(buf[:headerDecode.size])
                    if packetType == 1:
                        # dataPacket
                        aX,aY,aZ, gX,gY,gZ = frameDecode.unpack(buf[headerDecode.size:headerDecode.size + frameDecode.size])
                        buf = buf[headerDecode.size + frameDecode.size:]
                        ENGINE.updatePlots(DeviceID,aX,aY,aZ, gX,gY,gZ)
                    elif packetType == 2:
                        # MyowarePacket
                        rms,mav,zcr = myowareDecode.unpack(buf[headerDecode.size:headerDecode.size + myowareDecode.size])
                        rms = rms
                        mav= mav
                        zcr= zcr

                        # print(rms,mav,zcr)
                        buf = buf[headerDecode.size + myowareDecode.size:]
                        ENGINE.updatePlots('Myo',rms,mav,zcr,None,None,None)
                        # print(DeviceID, aX,aY,aZ, gX,gY,gZ)
            print("connection Closed")



    def runServer():
        print(":server RUN")
        HOST, PORT = "192.168.137.1", 4321
        # HOST, PORT = "192.168.1.100", 4321

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            print("Host: " + str(HOST) + " on port: " + str(PORT))
            server.timeout = 3
            server.serve_forever()



class classificationEngine():
    def __init__(self, sendResultsToServer):
        global IS_RUNNING_ON_ULTRA
        global IS_CONNECT_TO_ULTRA

        IS_RUNNING_ON_ULTRA = True
        IS_CONNECT_TO_ULTRA = False
        ENGINE.start()
        ENGINE.UlTRACallback = sendResultsToServer
        
        self.evalServerReplySet = ENGINE.evalServerReplySet
        pass

    def add_data(self, packet_type, d):
        if packet_type == "EMG":
            rms,mav,zcr = d
            ENGINE.updatePlots('Myo',rms,mav,zcr,None,None,None)
        if packet_type == "DATA":
            DeviceID,aX,aY,aZ, gX,gY,gZ = d
            DeviceID = int(DeviceID)
            ENGINE.updatePlots(DeviceID,aX,aY,aZ, gX,gY,gZ)

    

    


if __name__ == "__main__":
    if not IS_RUNNING_ON_ULTRA and IS_CONNECT_TO_ULTRA:
        try:
            ENGINE.start()
            connThread = Thread(target=ULTRA_CONN.run)
            connThread.run()
            if not IS_RUNNING_ON_ULTRA:
                runServer()
        except KeyboardInterrupt:
            _IS_KILL = True
            time.sleep(1)
            print('killing')
            sys.exit() 
    else:
        try:
            ce =classificationEngine(None)
            runServer()
                
        except KeyboardInterrupt:
            _IS_KILL = True
            time.sleep(1)
            print('killing')
            sys.exit()   
