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

# for saving results
rows = []

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

        # Remove noisy segments by amplitude
        amp_threshold_high = 1.8
        amp_threshold_low = 0.8
        mask = (ecg_data > amp_threshold_low) & (ecg_data < amp_threshold_high)
        ecg_data_trimmed = ecg_data[mask]

        # --- Plot both original and cleaned signals ---
        plt.figure(figsize=(14, 6))

        # Original ECG
        plt.subplot(2, 1, 1)
        plt.plot(ecg_data, color='blue', linewidth=0.8)
        plt.title(f"Original ECG ({pts}, {tsk})")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude (V)")

        # Cleaned ECG
        plt.subplot(2, 1, 2)
        plt.plot(ecg_data_trimmed, color='green', linewidth=0.8)
        plt.title(f"Trimmed ECG after amplitude-based removal ({pts}, {tsk})")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude (V)")

        plt.tight_layout()
        plt.show()

        # process the full time window
        signals_full, info = nk.ecg_process(ecg_data_trimmed, sampling_rate=1000)

        plt.figure(figsize=(14, 8))

        # 1) Raw signal
        plt.subplot(2, 1, 1)
        plt.plot(ecg_data_trimmed[40000:60000], linewidth=0.8)
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
        plt.close('all')

        # extract parameters using built-in analyzer
        results = nk.ecg_analyze(signals_full)
        print(results.keys())

        # Add identifiers
        results.insert(0, "Subject", pts)  # 0 = position index
        results.insert(1, "Session", tsk)  # 1 = position index

        # Store for later
        rows.append(results)   # store temporarily

df = pd.concat(rows, ignore_index=True)
outfile = os.path.join(resultsFolder, "ECG_results.csv")
df.to_csv(outfile, index=False)
print("Saved:", outfile)
