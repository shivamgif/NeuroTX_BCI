# %%
import sys
import biosig
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import mne
import csv
import math as m
# Loading the dataset
File = '/Users/shivam/Desktop/New Folder/content/A01T.gdf'
raw = mne.io.read_raw_gdf(File, preload=True, eog=(23, 24, 25))
HDR = biosig.header(File)
H = json.loads(HDR)

# %%
EEGDataset = biosig.data(File)
samplerate = 250.0
ListOfDataSamples = list()
ListOfLabels = list()
strtindx = 0
endindx = 0
for i in range(len(H["EVENT"])):
    StartOfTrial = H["EVENT"][i]
    try:
        StartOfAction = H["EVENT"][i+1]
    except:
        break

    # Start of a trail
    if(StartOfTrial['TYP'] == "0x0300"):
        # Cue onset left
        if(StartOfAction['TYP'] == "0x0301"):
            # Input Data Extraction
            strtindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate))
            endindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate + 1000))
            DataBlock = EEGDataset[strtindx:endindx, :]
            ListOfDataSamples.append(DataBlock)

            # Label computation
            Label = [1, 0, 0, 0]
            ListOfLabels.append(Label)

        # Cue onset right
        elif(StartOfAction['TYP'] == "0x0302"):
            # Input Data Extraction
            strtindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate))
            endindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate + 1000))
            DataBlock = EEGDataset[strtindx:endindx, :]
            ListOfDataSamples.append(DataBlock)

            # Label computation
            Label = [0, 1, 0, 0]
            ListOfLabels.append(Label)

        # Cue onset foot
        elif(StartOfAction['TYP'] == "0x0303"):
            # Input Data Extraction
            strtindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate))
            endindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate + 1000))
            DataBlock = EEGDataset[strtindx:endindx, :]
            ListOfDataSamples.append(DataBlock)

            # Label computation
            Label = [0, 0, 1, 0]
            ListOfLabels.append(Label)

        # Cue onset tongue
        elif(StartOfAction['TYP'] == "0x0304"):
            # Input Data Extraction
            strtindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate))
            endindx = int(m.ceil((StartOfTrial['POS']+2)*samplerate + 1000))
            DataBlock = EEGDataset[strtindx:endindx, :]
            ListOfDataSamples.append(DataBlock)

            # Label computation
            Label = [0, 0, 0, 1]
            ListOfLabels.append(Label)

Labels = np.array(ListOfLabels)
DataSamples = []
for k in ListOfDataSamples:
    for l in k:
        DataSamples.append(l)

Samples = np.array(DataSamples)
#Samples = np.reshape(Samples, (273, 1000, 25))

np.savetxt('Labels.csv', Labels, delimiter=",")
np.savetxt('DataSamples.csv', Samples, delimiter=",")
# %%
