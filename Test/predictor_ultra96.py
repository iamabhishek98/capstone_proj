# keras?
import os
import sys
import numpy as np

from Test.extractDataset import MAX_SAMPLES

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from FPGA.driver import fpga


class dancemove():
    def __init__(self, device, movename, timestamp,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List ):
        self.device = device
        self.movename = movename
        self.timestamp = timestamp

        self.a_xList = a_xList
        self.a_yList = a_yList
        self.a_zList = a_zList

        self.g_xList = g_xList
        self.g_yList = g_yList
        self.g_zList = g_zList
        
        self.activation_List = activation_List

    def getDataAsNumpyArray(self, norm = True):
            x = np.array(self.a_xList)
            y = np.array(self.a_yList)
            z = np.array(self.a_zList)
            x2 = np.array(self.g_xList)
            y2 = np.array(self.g_yList)
            z2 = np.array(self.g_zList)
            a = np.array(self.activation_List)

            if norm:
                NormLimit = 1
                x = (x+2)/4 * NormLimit
                y = (y+2)/4 * NormLimit
                z = (z+2)/4 * NormLimit

                x2 = (x2+250)/ (250 * 2) * NormLimit
                y2 = (y2+250)/ (250 * 2) * NormLimit
                z2 = (z2+250)/ (250 * 2) * NormLimit

                x = np.clip(x,0,NormLimit)
                y = np.clip(y,0,NormLimit)
                z = np.clip(z,0,NormLimit)

                x2 = np.clip(x2,0,NormLimit)
                y2 = np.clip(y2,0,NormLimit)
                z2 = np.clip(z2,0,NormLimit)


            
            f = [x,y,z,x2,y2,z2]
            return np.array(f)

class Predictor():
    def __init__(self, sendFunc):
        self.quickpredict = fpga()
        self.isMove = False
        self.samplesRecorded = 0

        self.a_xList = []
        self.a_yList = []
        self.a_zList = []

        self.g_xList = []
        self.g_yList = []
        self.g_zList = []
        
        self.activation_List = []

        self.sendFunc = sendFunc

    def clearBuffers(self):
        self.a_xList = []
        self.a_yList = []
        self.a_zList = []

        self.g_xList = []
        self.g_yList = []
        self.g_zList = []
        
        self.activation_List = []

    def startRecording( self ):
        print("Move Started")
        self.isMove = True
    
    def stopRecording( self ):
        if self.samplesRecorded < 50 :
            print("Move Ended. Too small")
            self.isMove = False
            self.samplesRecorded = 0
            self.clearBuffers()
        else:
            print("Move Ended. Predicting")
            self.predict()
            self.isMove = False
            self.samplesRecorded = 0
            self.clearBuffers()

    def updateCurrentMove(self,databuffer):
        if self.isMove:
            self.samplesRecorded +=1

            self.a_xList.extend(databuffer.a_xList[-3:])
            self.a_yList.extend(databuffer.a_yList[-3:])
            self.a_zList.extend(databuffer.a_zList[-3:])

            self.g_xList.extend(databuffer.g_xList[-3:])
            self.g_yList.extend(databuffer.g_yList[-3:])
            self.g_zList.extend(databuffer.g_zList[-3:])
        
            self.activation_List.extend(databuffer.activation_List[-3:])

    def predict(self):
        a_xList = self.a_xList[:MAX_SAMPLES]
        a_yList = self.a_yList[:MAX_SAMPLES]
        a_zList = self.a_zList[:MAX_SAMPLES]
        g_xList = self.g_xList[:MAX_SAMPLES]
        g_yList = self.g_yList[:MAX_SAMPLES]
        g_zList = self.g_zList[:MAX_SAMPLES]
        activation_List = self.activation_List[:MAX_SAMPLES]
        dm = dancemove("none", "none", 0,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
        inputdata = dm.getDataAsNumpyArray()
        print(inputdata.shape)
        inputdata = np.ravel(inputdata)
        inputdata= np.reshape(inputdata, (1,6*MAX_SAMPLES))
        inputdata = inputdata.tolist()
        results = self.quickpredict.predict(inputdata)
        print(inputdata.shape)
        print("softmax {}".format(results))
        npResults = np.array(results)
        finalIndex = np.argmax(npResults)

        predictionResult = ['gun', 'hair', 'sidepump'][finalIndex]

        if not (self.sendFunc == None):
            self.sendFunc(1,predictionResult)
    