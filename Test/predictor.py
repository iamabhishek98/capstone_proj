# keras?
import os
import tensorflow as tf
from tensorflow import keras
from extractDataset import *
import matplotlib.pyplot as plt


# prevents my com from using the gpu
def saveWeightstoFile(fname,weights):
    
    with open(fname, 'w') as f:
        w = list(map(lambda x: x.tolist(), weights))
        print(w, file=f)

class Predictor():
    def __init__(self):
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

        basepath = os.getcwd()
        modelfolder = 'chosenModel'
        fname = os.listdir('chosenModel')[0]
        fpath = os.path.join(basepath,modelfolder,fname )
        self.model = tf.keras.models.load_model(fpath)
        print(self.model.summary())
        saveWeightstoFile('current',self.model.get_weights() )

        self.isMove = False
        self.samplesRecorded = 0

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
            if (self.samplesRecorded == 0):
                self.samplesRecorded +=1

                self.a_xList.extend(databuffer.a_xList[-3:])
                self.a_yList.extend(databuffer.a_yList[-3:])
                self.a_zList.extend(databuffer.a_zList[-3:])

                self.g_xList.extend(databuffer.g_xList[-3:])
                self.g_yList.extend(databuffer.g_yList[-3:])
                self.g_zList.extend(databuffer.g_zList[-3:])
        
                self.activation_List.extend(databuffer.activation_List[-3:])
            else:
                self.samplesRecorded +=1

                self.a_xList.append(databuffer.a_xList[-1])
                self.a_yList.append(databuffer.a_yList[-1])
                self.a_zList.append(databuffer.a_zList[-1])

                self.g_xList.append(databuffer.g_xList[-1])
                self.g_yList.append(databuffer.g_yList[-1])
                self.g_zList.append(databuffer.g_zList[-1])
        
                self.activation_List.append(databuffer.activation_List[-1])

    def predict(self):
        a_xList = self.a_xList[:MAX_SAMPLES]
        a_yList = self.a_yList[:MAX_SAMPLES]
        a_zList = self.a_zList[:MAX_SAMPLES]
        g_xList = self.g_xList[:MAX_SAMPLES]
        g_yList = self.g_yList[:MAX_SAMPLES]
        g_zList = self.g_zList[:MAX_SAMPLES]
        activation_List = self.activation_List[:MAX_SAMPLES]
        dm = dancemove("none", "none", 0,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
        dm.getDataAsNumpyArray(Norm =False)
        inputdata = np.array(self.flatFeatures)
        print(inputdata.shape)
        for i in range(inputdata.shape[0])
            predData = inputdata[i]
            print(predData.shape)
            results = self.model.predict(predData)
            mlp_pred = np.argmax(results, axis=-1)[0]
            print("softmax {}".format(results))
            print("predicted value: {}".format(mlp_pred))
            # ['gun', 'hair', 'sidepump']
    