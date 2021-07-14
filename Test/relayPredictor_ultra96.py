import os
import sys
import numpy as np
from Test.extractionUtils import *

# from Test.extractDataset import MAX_SAMPLES

MAX_SAMPLES = 100
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from FPGA.driver import fpga
DANCENAMES_CLASSIFIER = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")


myFPGA = fpga()
class Predictor():
    def init(self):
        pass
    def predict(self, devName ,data):

        a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List = data
        dm = dancemove(devName, "none", 0,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
        dm.extractAllFeatures()
        inputdata = np.array(dm.flatFeatures)

        res = []
        for i in range(inputdata.shape[0]):
            predData = inputdata[i]
            predData= np.reshape(inputdata,(1,predData.shape[0]) )
            # print(predData)
            predData = predData.ravel().tolist()
            # print(predData)
            # print("INPUTS SHAPE:" , len(predData))
            results = myFPGA.predict(predData)
            # print(results)
            mlp_pred = np.argmax(results, axis=-1)
            res.append(DANCENAMES_CLASSIFIER[mlp_pred])
        print(res)
        return res[0]

        a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List = data
        dm = dancemove(devName, "none", 0,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
        inputdata = dm.getDataAsNumpyArray()
        # print("Classifying {}. Shape {}".format(devName, inputdata.shape))

        inputdata = np.ravel(inputdata)
        inputdata = inputdata.tolist()
        
        results = myFPGA.predict(inputdata)
        mlp_pred = np.argmax(results, axis=-1)
        # print("Classification Result: {} softMax: {}".format(DANCENAMES_CLASSIFIER[mlp_pred] ,results ))
        return DANCENAMES_CLASSIFIER[mlp_pred]