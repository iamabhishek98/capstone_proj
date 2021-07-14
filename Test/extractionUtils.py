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
import statistics
# from spectrum import aryule
from scipy.stats import kurtosis
from scipy.stats import skew

SLIDING_WINDOW_LENGTH = 100
SLIDING_WINDOW_STEP = 2
MAX_WINDOWS_PER_CLASS = 300

# Utility Functions
def get_mean(x):
    return np.mean(x)

def get_std(x):
    return np.std(x)

def get_var(x):
    return np.var(x)

def get_mag(x,y,z):
    temp = []
    for i in range(len(x)):
        temp.append((x[i]**2 +y[i]**2 +z[i]**2)**(0.5) - 1)
    return np.mean(temp)

def get_kurtosis(x):
    return kurtosis(x)

def get_skew(x):
    return skew(x)
    
def get_ptp(x):
    return np.ptp(x)

def get_idle_samples(x,y,z):
    temp = []
    for i in range(len(x)):
        temp.append(abs((x[i]**2 +y[i]**2 +z[i]**2)**(0.5) - 1))
    num = np.count_nonzero(np.array(temp) > 0.5)
    return num / SLIDING_WINDOW_LENGTH

def get_idle_samples2(x):
    mean = np.mean(x)
    num = np.count_nonzero(x > mean + 0.3)
    num2 = np.count_nonzero(x < mean - 0.3)
    return (num + num2)/ SLIDING_WINDOW_LENGTH


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
        
        # plt.show()
        # plt.clf()

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

    def plotNorm(self, show =True):
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

        d = self.getDataAsNumpyArray( norm = True)
        ax1, = accel.plot(index, d[0], label = "X")
        ax2, = accel.plot(index, d[1], label = "Y")
        ax3, = accel.plot(index, d[2], label = "Z")

        ax4, = gyro.plot(index, d[3], label = "X")
        ax5, = gyro.plot(index, d[4], label = "Y")
        ax6, = gyro.plot(index, d[5], label = "Z")

        ax7, = activation.plot(index, self.activation_List, label = "R")
        

        activation.set_xlim(xmin = 0 , xmax = len(self.activation_List) )
        activation.set_ylim(ymin = 0 , ymax = 2.2 )

        accel.set_xlim(xmin = 0 , xmax = len(self.activation_List) )
        accel.set_ylim(ymin = 0 , ymax = 1.1 )

        gyro.set_xlim(xmin = 0 , xmax = len(self.activation_List) )
        gyro.set_ylim(ymin = 0 , ymax = 1.1 )

        if show:
            plt.show(block = True)
            plt.clf()

    def plot(self, show =True):
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

        if show:
            plt.show(block = True)
            plt.clf()


    def plotFeatures(self, show =True, previousAxis = None):
        if previousAxis == None:
            fig = plt.figure()
            gs = gridspec.GridSpec(3, 4, width_ratios=[1,1,1,1], height_ratios=[0.2,1,1])
            index = [ x for x in range(len(self.activation_List))]
            # print(index)
            # TODO plot the activation
            activation = fig.add_subplot(gs[0,0])
            accel = fig.add_subplot(gs[1,0])
            gyro = fig.add_subplot(gs[2,0])

            aX_Feats = self.feats[1]
            axMean = aX_Feats[:,0]
            axStd = aX_Feats[:,1]
            axVar = aX_Feats[:,2]
            axKurt = aX_Feats[:,3]
            axSkew = aX_Feats[:,4]
            axPtp = aX_Feats[:,5]
            indexFeats = [ x for x in range(len(axMean))]
            
            featAxList = []
            axMean_plt = fig.add_subplot(gs[1,1])
            axMean_plt.set_title("Mean")
            axMean_plt.plot(indexFeats,axMean)
            featAxList.append(axMean_plt)

            axStd_plt = fig.add_subplot(gs[2,1])
            axStd_plt.set_title("std")
            axStd_plt.plot(indexFeats,axStd)
            featAxList.append(axStd_plt)

            axVar_plt = fig.add_subplot(gs[1,2])
            axVar_plt.set_title("Var")
            axVar_plt.plot(indexFeats,axVar)
            featAxList.append(axVar_plt)

            axKurt_plt = fig.add_subplot(gs[2,2])
            axKurt_plt.set_title("kurt")
            axKurt_plt.plot(indexFeats,axKurt)
            featAxList.append(axKurt_plt)

            axSkew_plt = fig.add_subplot(gs[1,3])
            axSkew_plt.set_title("skew")
            axSkew_plt.plot(indexFeats,axSkew)
            featAxList.append(axSkew_plt)

            axPtp_plt = fig.add_subplot(gs[2,3])
            axPtp_plt.set_title("Ptp")
            axPtp_plt.plot(indexFeats,axPtp)
            featAxList.append(axPtp_plt)

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

            if show:
                plt.show(block = True)
                plt.clf()
            return featAxList
        else:
            featAxList

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

    def get_data_len(self):
        mydata = self.get_data()
        assert all(len(x)==len(mydata[0]) for x in mydata)
        return len(mydata[0])

    def getSlidingWindow(self,ax,start):
        return ax[start:start+SLIDING_WINDOW_LENGTH]

    def extractAllFeatures(self , forPrediction = False):
            d = self.getDataAsNumpyArray(norm = True)
            aX = d[0]
            aY = d[1]
            aZ = d[2]
            gX = d[3]
            gY = d[4]
            gZ = d[5]

            aX_Feats = []
            aY_Feats = []
            aZ_Feats = []
            gX_Feats = []
            gY_Feats = []
            gZ_Feats = []
            
            l =  [
                (aX,aX_Feats),
                (aY,aY_Feats),
                (aZ,aZ_Feats),
                (gX,gX_Feats),
                (gY,gY_Feats),
                (gZ,gZ_Feats)
                ]
            flatFeatures = []
            count = 0
            for i in range(0,len(aX), SLIDING_WINDOW_STEP):
                count+=1
                if i+ SLIDING_WINDOW_LENGTH > len(aX):
                    break
                elif count > MAX_WINDOWS_PER_CLASS:
                    break
                flatFeaturesVector = []
                for axis,features in l:
                    win = self.getSlidingWindow(axis,i)
                    feat = self.extractFeaturesPerAxis(win)
                    features.append(feat)
                    flatFeaturesVector.extend(feat)
                mag_x = self.getSlidingWindow(aX,i)
                mag_y = self.getSlidingWindow(aY,i)
                mag_z = self.getSlidingWindow(aZ,i)

                flatFeaturesVector.append(get_mag(mag_x,mag_y,mag_z))
                flatFeaturesVector.append(get_idle_samples(mag_x,mag_y,mag_z))
                flatFeaturesVector.append(get_idle_samples2(mag_z))

                

                
                flatFeatures.append(flatFeaturesVector)
            self.flatFeatures = flatFeatures
            self.feats = (
                np.array(aX_Feats),
                np.array(aY_Feats),
                np.array(aZ_Feats),
                np.array(gX_Feats),
                np.array(gY_Feats),
                np.array(gZ_Feats)
            )
            return self.feats
    
    def extractFeaturesPerAxis(self, ax , p = False):
        axMean = get_mean(ax)
        axStd = get_std(ax)
        axVar = get_var(ax)
        axKurt = get_kurtosis(ax)
        axSkew = get_skew(ax)
        axPtp = get_ptp(ax)
        if p :
            print(axMean)
        return (axMean,axStd,axVar,axKurt,axSkew,axPtp)



    def getFeaturesAsListOfFlattenedArray(self):
        return self.flatFeatures
    
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
