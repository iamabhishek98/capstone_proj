# keras?
import os
import tensorflow as tf
from tensorflow import keras
from extractionUtils import *

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
SAVE_WEIGHTS = True
PREDICTOR_BASEPATH = os.getcwd()
MODEL_FOLDER = 'chosenModel'
DANCENAMES_CLASSIFIER = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")
fname = os.listdir('chosenModel')[0]
fpath = os.path.join(PREDICTOR_BASEPATH,MODEL_FOLDER,fname)
MODEL = tf.keras.models.load_model(fpath)
print("Loaded Model: {}".format(fpath))
print(MODEL.summary())
MAX_SAMPLES = 100

def saveWeightstoFile(fname,weights):
    with open(fname, 'w') as f:
        w = list(map(lambda x: x.tolist(), weights))
        print(w, file=f)

if SAVE_WEIGHTS:
    saveWeightstoFile('current',MODEL.get_weights())

class Predictor():
    def init(self):
        pass
    def predict(self, devName ,data):
        a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List = data
        dm = dancemove(devName, "none", 0,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
        dm.extractAllFeatures()
        inputdata = np.array(dm.flatFeatures)
        # print("Classifying {}. Shape {}".format(devName, inputdata.shape))
        res = []
        for i in range(inputdata.shape[0]):
            predData = inputdata[i]
            predData= np.reshape(inputdata,(1,predData.shape[0]) )
            results = MODEL.predict(predData)
            mlp_pred = np.argmax(results, axis=-1)[0]
            res.append(DANCENAMES_CLASSIFIER[mlp_pred])
        print(res)
        return res[0]
            # ['gun', 'hair', 'sidepump']
        inputdata = np.ravel(inputdata)
        inputdata= np.reshape(inputdata, (1,6*MAX_SAMPLES))
        results = MODEL.predict(inputdata)
        mlp_pred = np.argmax(results, axis=-1)[0]
        # print("Classification Result: {} softMax: {}".format(DANCENAMES_CLASSIFIER[mlp_pred] ,results ))
        return DANCENAMES_CLASSIFIER[mlp_pred]

if __name__ == "main":
    print("WEIGHTS")
    saveWeightstoFile('current',MODEL.get_weights())