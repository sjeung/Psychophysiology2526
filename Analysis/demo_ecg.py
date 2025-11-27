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

# where do we save the results?
resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
os.makedirs(resultsFolder, exist_ok=True)

# parameters
pts = 'sub-001'  # participants = ['sub-001']
tsk = 'baseline'  # tasks = ['baseline']

# assemble file name
filename = os.path.join(rawFolder, 'raw_demo-' + pts + '_' + tsk + '.txt')

# read in the data in respective conditions
print('reading in ' + filename)
subdata = pd.read_csv(filename)
ecg_data = subdata["ecg"].values

# RAW signal
plt.figure(figsize=(14, 4))
plt.plot(ecg_data[:20000], color='gray', label="Raw ECG")  # show first 2000 samples
plt.title("Raw ECG Signal")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.legend()
#plt.show()

# cleaned (filtered)
ecg_filtered = nk.ecg_clean(ecg_data, sampling_rate=sampling_rate, method="biosppy")

plt.figure(figsize=(14, 4))
plt.plot(ecg_data[:20000], color='gray', alpha=0.5, label="Raw ECG")
plt.plot(ecg_filtered[:20000], color='blue', label="Filtered ECG")
plt.title("Filtered ECG (Noise Removal)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.legend()
#plt.show()

# Detect R-peaks
ecg_peaks_dict = nk.ecg_findpeaks(ecg_filtered, sampling_rate=sampling_rate, method="neurokit")

# Extract R-peaks indices
rpeaks_idx = np.where(ecg_peaks_dict["ECG_R_Peaks"] == 1)[0]

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
#plt.show()

# Example: convert raw ECG to millivolts and remove DC offset
ecg_converted = (ecg_data - np.mean(ecg_data)) * 1000  # volts → mV, centered

# Clean ECG
ecg_filtered = nk.ecg_clean(ecg_converted, sampling_rate=sampling_rate, method="neurokit")

# Detect R-peaks
ecg_peaks = nk.ecg_findpeaks(ecg_filtered, sampling_rate=sampling_rate, method="neurokit")
rpeaks_idx = np.flatnonzero(ecg_peaks["ECG_R_Peaks"])

# Plot first 20000 samples
rpeaks_idx_plot = rpeaks_idx[rpeaks_idx < 20000]

plt.figure(figsize=(14, 4))
plt.plot(ecg_filtered[:20000], color='blue', label="Filtered ECG")
plt.scatter(rpeaks_idx_plot, ecg_filtered[rpeaks_idx_plot], color='red', label="R-peaks", zorder=5)
plt.title("R-peak Detection (Converted & Filtered ECG)")
plt.xlabel("Samples")
plt.ylabel("Amplitude (mV)")
plt.legend()
plt.show()

#ecg_signal = (ecg_signal - np.mean(ecg_signal)) * 1000
#eda_signal = (eda_signal - np.mean(eda_signal)) * scale
#emg_signal = np.abs(emg_signal - np.mean(emg_signal))


    # ECG: volts → mV, remove DC
    # signal_converted = (signal_volt - np.mean(signal_volt)) * 1000
    # EMG: volts → mV, remove DC, full-wave rectification
   # signal_converted = np.abs(signal_volt - np.mean(signal_volt)) * 1000
    # EDA: assume 0–2.5 V corresponds to 0–20 µS (example scaling)
   # signal_converted = (signal_volt - np.mean(signal_volt)) * (20 / adc_range)