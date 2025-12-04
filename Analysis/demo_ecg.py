import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import neurokit2 as nk
#from neurokit2 import misc as nk_misc, signal as nk_signal, ecg as nk_ecg
#NeuroKitWarning = nk_misc.NeuroKitWarning
#ecg_segment = nk_ecg.ecg_segment

sampling_rate = 1000

# where is your data folder?
dataFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Data'

# where is your raw data?
rawFolder = os.path.join(dataFolder, '01_raw-data')

# parameters
pts = 'sub-001'  # participants = ['sub-001']
tsk = 'baseline'  # tasks = ['baseline']

# assemble file name
filename = os.path.join(rawFolder, 'raw_demo-' + pts + '_' + tsk + '.txt')

# read in the data in respective conditions
print('reading in ' + filename)
subdata = pd.read_csv(filename)
raw_ecg_data = subdata["ecg"].values

# RAW signal
plt.figure(figsize=(14, 4))
plt.plot(raw_ecg_data[:20*sampling_rate], color='gray', label="Raw ECG")  # show first 2000 samples
plt.title("Raw ECG Signal")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

# Apply transfer function
sampling_resolution = 10
vcc = 3
gain = 1
ecg_data = (raw_ecg_data/2**(sampling_resolution-1) - 0.5) * vcc * gain

# Converted signal
plt.figure(figsize=(14, 4))
plt.plot(ecg_data[20*sampling_rate:40*sampling_rate], color='gray', label="ECG")  # show first 2000 samples
plt.title("Converted ECG Signal")
plt.xlabel("Samples")
plt.ylabel("Amplitude (V)")
plt.legend()
plt.show()

# cleaned (filtered)
ecg_filtered = nk.ecg_clean(ecg_data, sampling_rate=sampling_rate, method="neurokit")
bio_ecg_filtered = nk.ecg_clean(ecg_data, sampling_rate=sampling_rate, method="biosppy")

plt.figure(figsize=(14, 4))
#plt.plot(ecg_data[:20000], color='gray', alpha=0.5, label="Raw ECG")
plt.plot(ecg_filtered[:20000], color='blue', label="Filtered ECG")
plt.plot(bio_ecg_filtered[:20000], color='green', label="Filtered ECG using biosppy")
plt.title("Filtered ECG (Noise Removal)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

# Detect R-peaks
ecg_peaks_dict = nk.ecg_findpeaks(ecg_filtered, sampling_rate=sampling_rate, method="neurokit")

print(ecg_peaks_dict)

# Extract R-peaks indices
rpeaks_idx = ecg_peaks_dict["ECG_R_Peaks"]

# Plot
plt.figure(figsize=(14, 4))
plt.plot(ecg_filtered[:20000], color='blue', label="Filtered ECG")
plt.scatter(rpeaks_idx[rpeaks_idx < 20000],
            ecg_filtered[rpeaks_idx[rpeaks_idx < 20000]],
            color='red', label="R-peaks")
plt.title("R-peak Detection")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.legend()
plt.show()
