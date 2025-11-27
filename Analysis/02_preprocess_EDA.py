import pandas as pd
import matplotlib.pyplot as plt
import os
import neurokit2 as nk

dataFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Data'
rawFolder = os.path.join(dataFolder, '01_raw-data')

resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
os.makedirs(resultsFolder, exist_ok=True)

# parameters
pts = 'sub-001'
tsk = 'baseline'

# assemble file name
filename = os.path.join(rawFolder, 'raw_demo-' + pts + '_' + tsk + '.txt')

print('reading in ' + filename)

subdata = pd.read_csv(filename)
raw_eda_data = subdata["eda"].values

# Apply transfer function
VCC = 3.3
sampling_resolution = 10
eda_data = (raw_eda_data/2**sampling_resolution)*VCC/0.12

# preprocess
signals_eda, info_eda = nk.eda_process(eda_data, sampling_rate=1000)

plt.figure(figsize=(14, 8))

# 1) Raw EDA
plt.subplot(2, 1, 1)
plt.plot(eda_data[1:20000], linewidth=0.8)
plt.title("Raw EDA Signal (Unprocessed)")
plt.xlabel("Samples")
plt.ylabel("Amplitude (µS)")

# 2) Processed EDA
plt.subplot(2, 1, 2)
plt.plot(signals_eda["EDA_Clean"], linewidth=0.8, label="Clean EDA")
plt.plot(signals_eda["EDA_Tonic"], linewidth=0.8, label="Tonic (SCL)")
plt.plot(signals_eda["EDA_Phasic"], linewidth=0.8, label="Phasic (SCR)")
plt.title("Processed EDA (Cleaned, Tonic, Phasic)")
plt.xlabel("Samples")
plt.ylabel("Amplitude (µS)")
plt.legend()
plt.tight_layout()
#plt.savefig("...eda_preproc.png")
plt.show()

# neurokit summary
fig = nk.eda_plot(signals_eda)
plt.show()
