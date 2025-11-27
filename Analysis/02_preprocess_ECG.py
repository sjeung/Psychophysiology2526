import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from neurokit2 import misc as nk_misc, signal as nk_signal, ecg as nk_ecg

NeuroKitWarning = nk_misc.NeuroKitWarning
_signal_rate_plot = nk_signal.signal_rate._signal_rate_plot
_ecg_peaks_plot = nk_ecg.ecg_peaks._ecg_peaks_plot
ecg_segment = nk_ecg.ecg_segment

# where is your data folder?
dataFolder = r'P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\Data'

# where is your raw data?
rawFolder = os.path.join(dataFolder, '01_raw-data')

# where do we save the results?
resultsFolder = r'P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\Results'
os.makedirs(results_folder, exist_ok=True)

# parameters
participants = ['sub-001']
tasks = ['addition']

all_results = []

for pi in participants:
    for ti in tasks:
        for si in sessions:

            # assemble file name
            filename = os.path.join(rawFolder, 'raw_demo_' + pts + '_' + tsk + '.csv')

            # read in the data in respective conditions
            print('reading in ' + filename)
            subdata = pd.read_csv(filename, header=None, names=['ECG'], skiprows=1)

            # Extract the single column as a vector
            ecg_data = subdata['ECG'].values

            # process the full time window
            signals_full, info = nk.ecg_process(ecg_data, sampling_rate=1000)

            # select segment to plot
            ecg_signals = signals_full  # .iloc[50000:90000]

            # Following is modification of ecg_plot()
            # https://neuropsychology.github.io/NeuroKit/_modules/neurokit2/ecg/ecg_plot.html#ecg_plot

            # Extract R-peaks (take those from df as it might have been cropped)
            if "ECG_R_Peaks" in ecg_signals.columns:
                info["ECG_R_Peaks"] = np.where(ecg_signals["ECG_R_Peaks"] == 1)[0]

            # Prepare figure and set axes.
            gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[2 / 3, 1 / 3])
            fig = plt.figure(constrained_layout=False)
            ax0 = fig.add_subplot(gs[0, :-1])
            ax1 = fig.add_subplot(gs[1, :-1], sharex=ax0)
            ax2 = fig.add_subplot(gs[:, -1])

            # Plot signals
            phase = None
            if "ECG_Phase_Ventricular" in ecg_signals.columns:
                phase = ecg_signals["ECG_Phase_Ventricular"].values

            ax0 = _ecg_peaks_plot(
                ecg_signals["ECG_Clean"].values,
                info=info,
                sampling_rate=info["sampling_rate"],
                raw=ecg_signals["ECG_Raw"].values,
                quality=ecg_signals["ECG_Quality"].values,
                phase=phase,
                ax=ax0,
            )

            # Plot Heart Rate
            ax1 = _signal_rate_plot(
                ecg_signals["ECG_Rate"].values,
                info["ECG_R_Peaks"],
                sampling_rate=info["sampling_rate"],
                title="Heart Rate",
                ytitle="Beats per minute (bpm)",
                color="#FF5722",
                color_mean="#FF9800",
                color_points="#FFC107",
                ax=ax1,
            )

            # Plot individual heart beats
            ax2 = ecg_segment(
                ecg_signals,
                info["ECG_R_Peaks"],
                info["sampling_rate"],
                show="return",
                ax=ax2,
            )

            ax0.set_position([0.1, 0.9, 0.8, 0.2])
            ax1.set_position([0.1, 0.5, 0.8, 0.2])
            ax2.set_position([0.1, 0.1, 0.8, 0.2])

            # Save the current figure to a file
            figure_filename = results_folder + f'/{pi}_{ti}_{si}_ecg_nk.png'
            plt.savefig(figure_filename, bbox_inches='tight', pad_inches=0.1)  # Save the current active plot as a PNG file
            print(f"Saved figure to {figure_filename}")

            # Close the plot to free memory after saving
            plt.close()

            # process full length interval related data
            results = nk.ecg_intervalrelated(signals_full, sampling_rate=1000)
            print(results)

            # Append the results to the list with participant and condition as metadata
            results['Participant'] = pi
            results['Condition'] = ti + '_' + si
            all_results.append(results)

# Concatenate all the results into a single DataFrame
final_results = pd.concat(all_results, ignore_index=True)

# Save the concatenated DataFrame to a CSV file
output_filename = results_folder + 'ecg_results.csv'
final_results.to_csv(output_filename, index=False)

print(f"Saved results to {output_filename}")