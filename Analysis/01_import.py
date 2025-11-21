import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# This script is for reading in ECG, EDA, EMG data and restructuring them for further processing
# Files will be read in from Data/00_source-data folder
# and written in Data/00_raw-data folder

# count the number of header lines in txt file
header_lines = 3

# where is your data folder?
dataFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Data'

# where is your source data?
sourceFolder = os.path.join(dataFolder, '00_source-data')
rawFolder = os.path.join(dataFolder, '01_raw-data')

# create the target folder unless it exists already
if not os.path.exists(rawFolder):
    os.makedirs(rawFolder)

# 1. participants 1 and 2 : ECG and EDA

# participants and tasks
participants = ['sub-001', 'sub-002']
tasks = ['subtract', 'addition', 'baseline']

for pts in participants:
    for tsk in tasks:
        filename = os.path.join(sourceFolder, 'demo_' + pts + '_' + tsk + '.txt')

        # Load the last two columns (EDA and ECG)
        data = np.loadtxt(filename, skiprows=header_lines, usecols=(5, 6)) # -2, -1 : two last columns

        # Pick only the EDA and ECG
        eda = data[:, 0]
        ecg = data[:, 1]

        # Build a time axis
        fs = 1000  # samples per second
        t = np.arange(len(eda)) / fs # create "time" values in seconds

        # Plot EDA
        plt.figure()
        plt.plot(t, eda)
        plt.title("EDA Signal")
        plt.xlabel("Time")
        plt.ylabel("EDA")
        plt.show()

        # Plot ECG
        plt.figure()
        plt.plot(t, ecg)
        plt.title("ECG Signal")
        plt.xlabel("Time")
        plt.ylabel("ECG")
        plt.show()

        # Create a DataFrame
        df = pd.DataFrame({
            'time': t,
            'eda': eda,
            'ecg': ecg
        })

        # Save to CSV
        output_file = os.path.join(rawFolder, 'raw_demo-' + pts + '_' + tsk + '.txt')
        df.to_csv(output_file, index=False)  # index=False avoids writing row numbers

        print(f"CSV saved to {output_file}")

