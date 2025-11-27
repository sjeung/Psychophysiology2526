import pandas as pd
import matplotlib.pyplot as plt
import os
import neurokit2 as nk

# where is your data folder?
dataFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Data'

# where is your raw data?
rawFolder = os.path.join(dataFolder, '01_raw-data')

# where do we save the results?
resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
os.makedirs(resultsFolder, exist_ok=True)

# parameters
participants = ['sub-001', 'sub-002']
tasks = ['baseline', 'addition', 'subtract']

for pts in participants:
    for tsk in tasks:
        # assemble file name
        filename = os.path.join(rawFolder, 'raw_demo-' + pts + '_' + tsk + '.txt')

        # read in the data in respective conditions
        print('reading in ' + filename)
        subdata = pd.read_csv(filename)
        raw_ecg_data = subdata["ecg"].values

        # Apply transfer function (https://support.pluxbiosignals.com/knowledge-base/transfer-functions-converting-digital-sensor-data-into-physical-units/)
        sampling_resolution = 10
        vcc = 3
        gain = 1 # gain on website leads to an unreasonable unit
        ecg_data = (raw_ecg_data/2**(sampling_resolution-1) - 0.5) * vcc * gain

        # process the full time window
        signals_full, info = nk.ecg_process(ecg_data, sampling_rate=1000)

        plt.figure(figsize=(14, 8))

        # 1) Raw signal
        plt.subplot(2, 1, 1)
        plt.plot(ecg_data[40000:60000], linewidth=0.8)
        plt.title("Raw ECG Signal (Unprocessed)")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")

        # 2) Processed signal (NeuroKit output)
        plt.subplot(2, 1, 2)
        plt.plot(signals_full["ECG_Clean"][40000:60000], linewidth=0.8)
        plt.title("Processed ECG Signal (NeuroKit2: filtered + cleaned)")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.tight_layout()

        # save figure
        figures_folder = os.path.join(resultsFolder, 'figures')
        os.makedirs(figures_folder, exist_ok=True)
        figure_name = os.path.join(figures_folder, 'processed_ECG_' + pts + '_' + tsk + '.png')
        plt.savefig(figure_name)

        # Also show NeuroKit’s built-in ECG diagnostics plot
        fig = nk.ecg.ecg_plot(signals_full)
        figure_name = os.path.join(figures_folder, 'nk_summary_ECG_' + pts + '_' + tsk + '.png')
        plt.tight_layout()
        plt.savefig(figure_name)