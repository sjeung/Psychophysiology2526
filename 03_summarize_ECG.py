import pandas as pd
import matplotlib.pyplot as plt
import os
import neurokit2 as nk

resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
filename = os.path.join(resultsFolder, f'ECG_results.csv')
print(f'Reading {filename}...')

# Load data
alldata = pd.read_csv(filename)
