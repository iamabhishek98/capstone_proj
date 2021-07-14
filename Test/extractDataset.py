import sys
import os
import csv
import numpy as np
import pandas as pd
import random

import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec

from sklearn import preprocessing
from sklearn import decomposition

from extractionUtils import *

IMPORTED_BY_OTHER_MOD =True
from relayMain import DeviceDataBuffer , MIN_MOVE_TIME_SAMPLES



# Definitions
BASEPATH = os.getcwd()
SAVEFOLDER = 'raw'
TESTFOLDER = 'testRaw'
PROCESSEDFOLDER = 'processed'
DANCEMOVENAMES = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")
IS_RETURN_DATAFRAME =False

### ===========PROCESSING CONFIG=============== ###

#Number of samples to include in dance move after end detected
NUMBER_OF_AFTER_SAMPLES = 0
#Number of samples to include in dance move before start detected
NUMBER_OF_BEFORE_SAMPLES = 20
# NUMBER_OF_BEFORE_SAMPLES = 5

#Minimum number of samples to be considered a move. Set this too low and you will get garbage dance samples
MINIMUM_MOVE_TIME = MIN_MOVE_TIME_SAMPLES 

#Pad recordings that are too short (ie. recording ends too quickly, not enough neutral samples)
IS_PAD = False
#Number of samples to pad
PAD_NUM =20

#If true, all dance moves will contain MAX_SAMPLES number of samples
USE_MAX_SAMPLES = False
#Number of samples per dance move
MAX_SAMPLES = 100


#Use temporal data augmentation (does not make sense for final evaluation architecture)
USETEMP = True
#Number of temporal Augmentations
TEMPORALDATAAUGNUM = 5

#Use acceleration Data Augmentation
USEACCEL= True
#Number of acceleration Data Augmentations
NUMRANDOMSHIFTSACCEL = 20
#Maximum shift in the z axis for acceleration Data Augmentation
Z_RAND_MAX = 0.2

class tempDataBuffer(DeviceDataBuffer):
    def __init__(self, devName, buffersize):
        super().__init__(devName, internalBufferSize = buffersize)

    def updatePredictor(self):
        return None
    def updateRecorder(self):
        return None
    def sendSample(self):
        return None

def listFiles(savepath =SAVEFOLDER ):
    filepath = os.path.join(BASEPATH, savepath)
    return os.listdir(filepath)

def extractFileMetadata(fname):
    device, movename, timestamp = fname.split("_")
    return (device, movename, timestamp)

def readRawDataset(fname, savepath = SAVEFOLDER ):
    filepath = os.path.join(BASEPATH, savepath, fname)

    dataset = {
        'a_xList': [],
        'a_yList': [],
        'a_zList': [],
        'g_xList': [],
        'g_yList': [],
        'g_zList': [],
        'activation_List': []
    }
    with open(filepath, 'r', newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in csvReader:
            # print(row)
            if count == 0:
                count += 1
                continue
            dataset['a_xList'].append(float(row[0]))
            dataset['a_yList'].append(float(row[1]))
            dataset['a_zList'].append(float(row[2]))
            dataset['g_xList'].append(float(row[3]))
            dataset['g_yList'].append(float(row[4]))
            dataset['g_zList'].append(float(row[5]))
            dataset['activation_List'].append(int(row[6]))
            count += 1
        if IS_PAD:
            for i in range(PAD_NUM):
                dataset['a_xList'].insert(0,dataset['a_xList'][0])
                dataset['a_yList'].insert(0,dataset['a_yList'][0])
                dataset['a_zList'].insert(0,dataset['a_zList'][0])
                dataset['g_xList'].insert(0,dataset['g_xList'][0])
                dataset['g_yList'].insert(0,dataset['g_yList'][0])
                dataset['g_zList'].insert(0,dataset['g_zList'][0])
                dataset['activation_List'].insert(0,dataset['activation_List'][0])

                dataset['a_xList'].append(dataset['a_xList'][-1])
                dataset['a_yList'].append(dataset['a_yList'][-1])
                dataset['a_zList'].append(dataset['a_zList'][-1])
                dataset['g_xList'].append(dataset['g_xList'][-1])
                dataset['g_yList'].append(dataset['g_yList'][-1])
                dataset['g_zList'].append(dataset['g_zList'][-1])
                dataset['activation_List'].append(dataset['activation_List'][-1])


        device, movename, timestamp = extractFileMetadata(fname)
        print("Recording from {} with move {} at {} opened with {} samples".format(device, movename,timestamp ,count - 1))

        r = rawDataset(device, movename, timestamp, dataset)

        recalulated = recaluculateDatasetActivations(device + "recal", movename, timestamp, r)

        # r.plot()
        # recalulated.plot()
        # plt.show()
        # plt.clf()
        return recalulated

def recaluculateDatasetActivations(devName, movename, timestamp, d: rawDataset):
    devData = d.dataset

    mybuff = tempDataBuffer(devName, len(devData['a_xList']))
    
    for i in range(len(devData['a_xList'])):
        aX = devData['a_xList'][i]
        aY = devData['a_yList'][i]
        aZ = devData['a_zList'][i]
        gX = devData['g_xList'][i]
        gY = devData['g_yList'][i]
        gZ = devData['g_zList'][i]
        mybuff.updateInternalState(aX,aY,aZ,gX,gY,gZ)
    dataset = {
        'a_xList': mybuff.aX,
        'a_yList': mybuff.aY,
        'a_zList': mybuff.aZ,
        'g_xList': mybuff.gX,
        'g_yList': mybuff.gY,
        'g_zList': mybuff.gZ,
        'activation_List': mybuff.actList
    }
    return rawDataset(devName, movename, timestamp, dataset)


    


def isolateSequences(rawdata, useAccelBaseValueAugmentation =True , useTemporalAugmentation =True):
    moveIdxs = []
    device = rawdata.device
    movename = rawdata.movename
    timestamp = rawdata.timestamp
    d = rawdata.dataset

    numberOfSamples = len(d['a_xList'])
    isInMove=False
    startIdx = None
    endIdx = None
    for idx in range(numberOfSamples):
        currentActivation = d['activation_List'][idx]
        if (currentActivation == 2) and (isInMove == False):
            isInMove = True
            startIdx = idx
            cooldown = MINIMUM_MOVE_TIME
        elif (isInMove == True) and ((not currentActivation == 2) or idx == numberOfSamples-1 ):
            isInMove = False
            endIdx = idx
            moveIdxs.append( (startIdx,endIdx ) )

    movesData = []
    for start,end in moveIdxs:
        
        if (end - start) < MINIMUM_MOVE_TIME:
            print("???")
            continue

        if USE_MAX_SAMPLES:
            if useTemporalAugmentation:
                for i in range(-TEMPORALDATAAUGNUM,(TEMPORALDATAAUGNUM+1)*10,2 ):
                    print(len(d['a_xList']))
                    localStart = start - NUMBER_OF_BEFORE_SAMPLES
                    requiresPad = 0
                    if localStart<0:
                        requiresPad = abs(localStart)
                        localStart = 0
                    localEnd = localStart + MAX_SAMPLES
                    a_xList = d['a_xList'][localStart+i:localEnd+i]
                    a_yList = d['a_yList'][localStart+i:localEnd+i]
                    a_zList = d['a_zList'][localStart+i:localEnd+i]
                    g_xList = d['g_xList'][localStart+i:localEnd+i]
                    g_yList = d['g_yList'][localStart+i:localEnd+i]
                    g_zList = d['g_zList'][localStart+i:localEnd+i]
                    activation_List = d['activation_List'][localStart+i:localEnd+i]

                    if len(a_xList)==0 or len(a_xList) != MAX_SAMPLES:
                        print("DATAERROR")
                        print(len(a_xList),len(a_yList),len(a_zList),len(g_xList),len(g_yList),len(g_zList) )
                        print(len(d['a_xList']),len( d['a_yList']),len(d['a_zList']),len(d['g_xList']),len(d['g_yList']),len(d['g_zList']) )
                        print(localStart+i,localEnd+i)
                        assert False
                    dm = dancemove(device, movename, timestamp,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
                    movesData.append(dm)
                if useAccelBaseValueAugmentation:
                    for i in range(NUMRANDOMSHIFTSACCEL):
                        localStart = start - NUMBER_OF_BEFORE_SAMPLES
                        localEnd = localStart + MAX_SAMPLES

                        z_rand = random.uniform(0, Z_RAND_MAX)
                        y_rand = random.uniform(0, z_rand)
                        x_rand = z_rand - y_rand

                        a_xList = list( map( lambda x: x + x_rand, a_xList) )
                        a_yList = list( map( lambda x: x + y_rand, a_yList) )
                        a_zList = list( map( lambda x: x - z_rand, a_zList) )

                        # g_xList = d['g_xList'][localStart:localEnd]
                        # g_yList = d['g_yList'][localStart:localEnd]
                        # g_zList = d['g_zList'][localStart:localEnd]
                        # activation_List = d['activation_List'][localStart:localEnd]
                        dm = dancemove(device, movename, timestamp,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
                        movesData.append(dm)

            if not useAccelBaseValueAugmentation and not useTemporalAugmentation:
                    localStart = start - NUMBER_OF_BEFORE_SAMPLES
                    localEnd = localStart + MAX_SAMPLES
                    a_xList = d['a_xList'][localStart:localEnd]
                    a_yList = d['a_yList'][localStart:localEnd]
                    a_zList = d['a_zList'][localStart:localEnd]
                    g_xList = d['g_xList'][localStart:localEnd]
                    g_yList = d['g_yList'][localStart:localEnd]
                    g_zList = d['g_zList'][localStart:localEnd]
                    activation_List = d['activation_List'][localStart:localEnd]
                    dm = dancemove(device, movename, timestamp,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
                    movesData.append(dm)

        else:
            
            a_xList = d['a_xList'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]
            a_yList = d['a_yList'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]
            a_zList = d['a_zList'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]
            g_xList = d['g_xList'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]
            g_yList = d['g_yList'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]
            g_zList = d['g_zList'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]
            activation_List = d['activation_List'][start - NUMBER_OF_BEFORE_SAMPLES: end + NUMBER_OF_AFTER_SAMPLES ]


            dm = dancemove(device, movename, timestamp,a_xList,a_yList,a_zList,g_xList,g_yList,g_zList,activation_List)
            movesData.append(dm)
    return movesData

def processData( testset =False):
    if not testset:
        raws = list(map(lambda x:readRawDataset(x), listFiles()))
    else:
        raws = list(map(lambda x:readRawDataset(x ,savepath= TESTFOLDER), listFiles(savepath= TESTFOLDER)))

    combinedList = []
    numberOfMoves = 0
    for item in raws:
        # item.plot()
        moves = isolateSequences(item, useTemporalAugmentation = USETEMP, useAccelBaseValueAugmentation= USEACCEL )
        if len(moves) == 0:
            # item.plot()
            # plt.show()
            # plt.clf()
            pass
        numberOfMoves += len(moves)
        combinedList.extend(moves)
    print("Done")
    print("Extracted {} moves from {} raw data Sequences.".format(numberOfMoves, len(raws)))

    numberOfEachMoves = dict.fromkeys(DANCEMOVENAMES ,0)
    numberOfEachMoves["defaultMove"] = 0
    for item in combinedList:
        numberOfEachMoves[item.movename] += 1
        
    for k,v in numberOfEachMoves.items():
        print("{}  {}".format(v, k))

    # for item in combinedList:
    #     item.plot()

    # for idx,item in enumerate(combinedList):
    #     item.writeThisFile(idx)   
  
    if IS_RETURN_DATAFRAME:
        frame = pd.DataFrame()
        c = list(map(lambda x : x.toDict(),combinedList ))
        for df in c:
            frame = frame.append(df, ignore_index=True)
        return frame

    return combinedList

if __name__ == "__main__":
    danceMoveDataset = processData(testset=False)

    indexedMoves = {}
    for idx,dance in enumerate(DANCEMOVENAMES):
        indexedMoves[dance] = idx +1

    x = []
    y = []
    for i in danceMoveDataset:
        i.extractAllFeatures()
        # i.plotFeatures(show = False)
        flatArray = np.array(i.flatFeatures)
        print(flatArray.shape)
        x.extend(flatArray)
        y.extend([indexedMoves[i.movename]]*flatArray.shape[0])
    
    arrX = np.array(x)
    print(arrX.shape)

    print(np.amax(arrX, axis = 0) , np.amax(arrX, axis = 0).shape )
    print(np.amin(arrX, axis = 0),np.amin(arrX, axis = 0).shape )

    # pca = decomposition.PCA(n_components=17)
    # pca.fit(x)
    # x = pca.transform(x)
    
    # fig = plt.figure(1, figsize=(4, 3))
    # ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

    # ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=y, cmap=plt.cm.nipy_spectral,
    #         edgecolor='k')
    # plt.show()
    # plt.clf()