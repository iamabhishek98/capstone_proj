import sys
import os
import csv
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec



# Definitions
BASEPATH = os.getcwd()
SAVEFOLDER = 'raw'
PROCESSEDFOLDER = 'processed'
DANCEMOVENAMES = ("dab","elbowkick","gun","hair","listen","pointhigh","sidepump","wipetable")
IS_RETURN_DATAFRAME =True

#Changeable Parameters
NUMBER_OF_AFTER_SAMPLES = 5 #Number of samples to include in dance move after end detected
NUMBER_OF_BEFORE_SAMPLES = 5 #Number of samples to include in dance move before start detected
MINIMUM_MOVE_TIME =10 #Minimum number of samples to be considered a move. Set this too low and you will get garbage dance samples

class rawDataset():
    def __init__(self, device, movename, timestamp, dataset):
        self.device = device
        self.movename = movename
        self.timestamp = timestamp
        self.dataset = dataset
    def plot(self):
        fig = plt.figure()
        gs = gridspec.GridSpec(3, 1, width_ratios=[1], height_ratios=[0.2,1,1])
        index = [ x for x in range(len(self.dataset['activation_List']))]
        # print(index)
        # TODO plot the activation
        activation = fig.add_subplot(gs[0])
        accel = fig.add_subplot(gs[1])
        gyro = fig.add_subplot(gs[2])

        activation.set_title("Device " + str(self.device) + "\nActivation" )
        accel.set_title("Accel" )
        gyro.set_title("Gyro" )


        ax1, = accel.plot(index, self.dataset['a_xList'], label = "X")
        ax2, = accel.plot(index, self.dataset['a_yList'], label = "Y")
        ax3, = accel.plot(index, self.dataset['a_zList'], label = "Z")

        ax4, = gyro.plot(index, self.dataset['g_xList'], label = "X")
        ax5, = gyro.plot(index, self.dataset['g_yList'], label = "Y")
        ax6, = gyro.plot(index, self.dataset['g_zList'], label = "Z")

        ax7, = activation.plot(index, self.dataset['activation_List'], label = "R")
        
        displaylen = len(self.dataset['activation_List'])

        activation.set_xlim(xmin = 0 , xmax = displaylen )
        activation.set_ylim(ymin = 0.2 , ymax = 2.2 )

        accel.set_xlim(xmin = 0 , xmax = displaylen )
        accel.set_ylim(ymin = -2 , ymax = 2 )

        gyro.set_xlim(xmin = 0 , xmax = displaylen )
        gyro.set_ylim(ymin = -250 , ymax = 250 )
        
        plt.show()

    
        plt.clf()


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

    def toDict(self):
        d = dict()
        d['movename'] = self.movename
        d['a_xList'] = self.a_xList
        d['a_yList'] = self.a_yList
        d['a_zList'] = self.a_zList
        d['g_xList'] = self.g_xList
        d['g_yList'] = self.g_yList
        d['g_zList'] = self.g_zList
        d['activation_List'] = self.activation_List
        return d

    def writeThisFile(self,moveid):
        fname = "{}_{}_{}_{}".format(self.device, self.movename, self.timestamp, str(moveid))
        f = os.path.join(BASEPATH,PROCESSEDFOLDER,fname ) 
        if not os.path.exists(os.path.dirname(f)):
            try:
                os.makedirs(os.path.dirname(f))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(f, 'w', newline='') as csvfile:
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

    def plot(self):
        fig = plt.figure()
        gs = gridspec.GridSpec(3, 1, width_ratios=[1], height_ratios=[0.2,1,1])
        index = [ x for x in range(len(self.activation_List))]
        # print(index)
        # TODO plot the activation
        activation = fig.add_subplot(gs[0])
        accel = fig.add_subplot(gs[1])
        gyro = fig.add_subplot(gs[2])

        activation.set_title("{} {} {}".format(self.device, self.movename, self.timestamp) )
        accel.set_title("Accel" )
        gyro.set_title("Gyro" )
        # print( self.a_xList)

        ax1, = accel.plot(index, self.a_xList, label = "X")
        ax2, = accel.plot(index, self.a_yList, label = "Y")
        ax3, = accel.plot(index, self.a_zList, label = "Z")

        ax4, = gyro.plot(index, self.g_xList, label = "X")
        ax5, = gyro.plot(index, self.g_yList, label = "Y")
        ax6, = gyro.plot(index, self.g_zList, label = "Z")

        ax7, = activation.plot(index, self.activation_List, label = "R")
        

        activation.set_xlim(xmin = 0 , xmax = len(self.activation_List) )
        activation.set_ylim(ymin = 0.2 , ymax = 2.2 )

        accel.set_xlim(xmin = 0 , xmax = len(self.activation_List) )
        accel.set_ylim(ymin = -2 , ymax = 2 )

        gyro.set_xlim(xmin = 0 , xmax = len(self.activation_List) )
        gyro.set_ylim(ymin = -250 , ymax = 250 )

        plt.show(block = True)
        plt.clf()

    def print_Data(self):
        print(self.activation_List)

    def get_label(self):
        return self.movename

    def get_data(self):
        return [
            self.a_xList,
            self.a_yList,
            self.a_zList,
            self.g_xList,
            self.g_yList,
            self.g_zList,
            self.activation_List
        ] 


def listFiles():
    filepath = os.path.join(BASEPATH, SAVEFOLDER)
    return os.listdir(filepath)

def extractFileMetadata(fname):
    device, movename, timestamp = fname.split("_")
    return (device, movename, timestamp)

def readRawDataset(fname):
    filepath = os.path.join(BASEPATH, SAVEFOLDER, fname)

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
        device, movename, timestamp = extractFileMetadata(fname)
        print("Recording from {} with move {} at {} opened with {} samples".format(device, movename,timestamp ,count - 1))

        r = rawDataset(device, movename, timestamp, dataset)
        return r

def isolateSequences(rawdata):
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
        elif (isInMove == True) and (not currentActivation == 2):
            isInMove = False
            endIdx = idx
            moveIdxs.append( (startIdx,endIdx ) )

    movesData = []
    for start,end in moveIdxs:
        if (end - start) < MINIMUM_MOVE_TIME:
            continue
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



def processData():
    raws = list(map(lambda x:readRawDataset(x), listFiles()))
    combinedList = []
    numberOfMoves = 0
    for item in raws:
        # item.plot()
        moves = isolateSequences(item)
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
        # item.plot()

    for idx,item in enumerate(combinedList):
        item.writeThisFile(idx)   
  
    if IS_RETURN_DATAFRAME:
        frame = pd.DataFrame()
        c = list(map(lambda x : x.toDict(),combinedList ))
        for df in c:
            frame = frame.append(df, ignore_index=True)


        return frame

    return combinedList



if __name__ == "__main__":
    danceMoveDataset = processData()
    # TODO: take not that ML guys. danceMoveDataset contains the data you want. If you want to, you can pickle this list