# Check out https://mne.tools/stable/auto_tutorials/evoked/30_eeg_erp.html

import mne
import os

epoched_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\03_epoched"

ses = "oddballstand"

# Load ERPs
epoched_path = os.path.join(epoched_folder, f"sub-001_ses-{ses}_epoched.fif")
epochs = mne.read_epochs(epoched_path)
print(epochs.ch_names)

# take standard locations
epochs.set_montage("standard_1020")

# average the target and standard epochs respectively
evoked_target = epochs["target"].average()
evoked_standard = epochs["standard"].average()

# visualize data from all channels
evoked_target.plot(spatial_colors=True)
evoked_target.plot_topomap(times=[-0.2, 0.1, 0.4], average=0.05)
evoked_standard.plot(spatial_colors=True)
evoked_standard.plot_topomap(times=[-0.2, 0.1, 0.4], average=0.05)

# summary plot
#evokeds = dict(
#    standard=list(epochs["standard"].iter_evoked()),
#    target=list(epochs["target"].iter_evoked()),
#)
#mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=picks)