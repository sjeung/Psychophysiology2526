import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import neurokit2 as nk

dataFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Data'
rawFolder = os.path.join(dataFolder, '01_raw-data')

resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
os.makedirs(resultsFolder, exist_ok=True)

participants = ['sub-003', 'sub-004']
tasks        = ['baseline', 'stand', 'semitandem']

# loop through all fields
for pts in participants:
    for tsk in tasks:
        filename = os.path.join(rawFolder, f'raw_demo-{pts}_{tsk}.txt')
        print(f'Reading {filename}...')

        # Load data
        subdata = pd.read_csv(filename)
        emg_data_raw = subdata["emg"].values

        # Apply transfer function https://support.pluxbiosignals.com/wp-content/uploads/2021/11/electromyography-emg-user-manual.pdf
        VCC = 3.3
        sampling_resolution = 10
        G = 1009 # sensor gain
        emg_data = (emg_data_raw/(2**sampling_resolution)-0.5)*VCC*1000/G

        signals_emg, info_emg = nk.emg_process(emg_data, sampling_rate=1000)

        # Plot EMG signals
        plt.figure(figsize=(14, 8))

        # 1) Raw EMG
        plt.subplot(2, 1, 1)
        plt.plot(emg_data[:20000], linewidth=0.8)
        plt.title(f"Raw EMG Signal ({pts}, {tsk})")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")

        # 2) Processed EMG
        plt.subplot(2, 1, 2)
        #plt.plot(signals_emg["EMG_Raw"], linewidth=0.8, label="Raw EMG")
        plt.plot(signals_emg["EMG_Clean"][:20000], linewidth=0.8, label="Clean EMG")
        plt.title(f"Processed EMG ({pts}, {tsk})")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()

        # save figure
        figures_folder = os.path.join(resultsFolder, 'figures')
        os.makedirs(figures_folder, exist_ok=True)
        figure_name = os.path.join(figures_folder, 'processed_EMG_' + pts + '_' + tsk + '.png')
        plt.savefig(figure_name)

        if np.any(signals_emg["EMG_Activity"] == 1):
            fig = nk.emg_plot(signals_emg)
            figure_name = os.path.join(figures_folder, 'nk_summary_EMG_' + pts + '_' + tsk + '.png')
            plt.savefig(figure_name)
        else:
            print("No EMG bursts detected — skipping burst visualization.")