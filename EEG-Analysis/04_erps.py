# Check out https://mne.tools/stable/auto_tutorials/evoked/30_eeg_erp.html

import mne
import os

epoched_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\03_epoched"

sessions = ["oddballstand", "oddballwalk"]
diff_trials_dict = {}  # store lists of per-trial diff Evokeds

for ses in sessions:
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

    # summary plot within session
    picks = ["Fz", "Cz"] # for auditory processing and mismatch negativity ["Cz", "Pz"] for P300 in target condition
    evokeds = dict(
        standard=list(epochs["standard"].iter_evoked()),
        target=list(epochs["target"].iter_evoked()),
    )

    mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=picks)

    # get per-trial evokeds
    evokeds_target = list(epochs["target"].iter_evoked())
    evokeds_standard = list(epochs["standard"].iter_evoked())

    # compute difference per trial
    evokeds_diff_trials = [
        mne.combine_evoked([t, s], weights=[1, -1])
        for t, s in zip(evokeds_target, evokeds_standard)
    ]

    diff_trials_dict[ses] = evokeds_diff_trials

# Plot difference waves between sessions
figs = mne.viz.plot_compare_evokeds(
    diff_trials_dict,
    picks=picks,
    combine="mean",
    ci=True,
    colors={"oddballstand": "green", "oddballwalk": "red"},
    title="Target - Standard: Walking vs Standing",
    show=True
)

# figs is a list of Figure objects for some reason ...
for i, fig in enumerate(figs):
    fig.savefig(os.path.join(epoched_folder, f"diff_ERP_{i}.png"), dpi=300)