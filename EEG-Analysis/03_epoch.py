import re
import os
import mne
from mne import Annotations

# Paths
preprocessed_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\02_preprocessed"
epoched_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\03_epoched"
os.makedirs(epoched_folder, exist_ok=True)

# Parameters
tmin, tmax = -0.2, 0.8
baseline = (-0.2, 0)

sessions = ["oddballstand", "oddballwalk"]

for ses in sessions:
    # Load preprocessed data
    preproc_path = os.path.join(preprocessed_folder, f"sub-001_ses-{ses}_preprocessed.fif")
    eeg = mne.io.read_raw_fif(preproc_path, preload=True)

    # inspect the first ten "annotations" (= events)
    print(eeg.annotations.description[:10])

    # process events and extract behavioural data
    new_onsets = []
    new_durations = []
    new_desc = []
    standard_onsets = []
    target_onsets = []
    response_onsets = []

    for onset, duration, desc in zip(
            eeg.annotations.onset,
            eeg.annotations.duration,
            eeg.annotations.description):

        # extract etype and ecode
        etype_match = re.search(r"<etype>(.*?)</etype>", desc)
        ecode_match = re.search(r"<ecode>(.*?)</ecode>", desc)

        if not etype_match or not ecode_match:
            continue

        etype = etype_match.group(1)
        ecode = ecode_match.group(1)

        # keep only relevant events
        if etype == "Sound" and ecode == "sta":
            label = "standard"
            standard_onsets.append(onset)
        elif etype == "Sound" and ecode == "tar":
            label = "target"
            target_onsets.append(onset)
        elif etype == "Response" and ecode == "33":  # take the first response and ignore duplicate
            label = "response"
            response_onsets.append(onset)
        else:
            continue

        new_onsets.append(onset)
        new_durations.append(duration)
        new_desc.append(label)

    # replace annotations
    eeg.set_annotations(
        Annotations(new_onsets, new_durations, new_desc)
    )
    events, event_id = mne.events_from_annotations(eeg) # to work in mne style structure

    # only epoch sound events
    event_id_sound = {
        "standard": event_id["standard"],
        "target": event_id["target"]
    }

    epochs = mne.Epochs(
        eeg,
        events,
        event_id=event_id_sound,
        tmin=tmin,
        tmax=tmax,
        baseline=baseline,
        preload=True
    )

    # save epoched data
    epoched_path = os.path.join(epoched_folder, f"sub-001_ses-{ses}_epoched.fif")
    epochs.save(epoched_path, overwrite=True)