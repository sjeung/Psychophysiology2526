import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import neurokit2 as nk
from neurokit2 import misc as nk_misc, signal as nk_signal, ecg as nk_ecg

NeuroKitWarning = nk_misc.NeuroKitWarning
#_signal_rate_plot = nk_signal.signal_rate._signal_rate_plot
#_ecg_peaks_plot = nk_ecg.ecg_peaks._ecg_peaks_plot
ecg_segment = nk_ecg.ecg_segment

# where is your data folder?
dataFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Data'

# where is your raw data?
rawFolder = os.path.join(dataFolder, '01_raw-data')

# where do we save the results?
resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
os.makedirs(resultsFolder, exist_ok=True)

# parameters
pts = 'sub-001' #participants = ['sub-001']
tsk = 'baseline' #tasks = ['baseline']

# assemble file name
filename = os.path.join(rawFolder, 'raw_demo-' + pts + '_' + tsk + '.txt')

# read in the data in respective conditions
print('reading in ' + filename)
subdata = pd.read_csv(filename)
ecg_data = subdata["ecg"].values

# process the full time window
signals_full, info = nk.ecg_process(ecg_data, sampling_rate=1000)

# select segment to plot
# ecg_signals = signals_full[1:20000]  # .iloc[50000:90000]

plt.figure(figsize=(14, 8))

# 1) Raw signal
plt.subplot(2, 1, 1)
plt.plot(ecg_data[1:20000], linewidth=0.8)
plt.title("Raw ECG Signal (Unprocessed)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

# 2) Processed signal (NeuroKit output)
plt.subplot(2, 1, 2)
plt.plot(signals_full["ECG_Clean"][:20000], linewidth=0.8)
plt.title("Processed ECG Signal (NeuroKit2: filtered + cleaned)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.tight_layout()
#plt.save("-.png")
plt.show()

# Also show NeuroKit’s built-in ECG diagnostics plot
#fig = nk.ecg.ecg_plot(signals_full)
#plt.show()