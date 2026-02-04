import os
from mne_bids import BIDSPath, read_raw_bids

# Path to your BIDS root folder
bids_root = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\00_source-data"
raw_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\01_raw-data"
os.makedirs(raw_folder, exist_ok=True)

sub = "001"
ses = "oddballstand"

bids_path = BIDSPath(
    subject=sub,
    session=ses,
    task="Oddball",
    datatype="eeg",
    root=bids_root
)

# Read the data
raw = read_raw_bids(
    bids_path=bids_path
)

print(raw)

# Drop last 3 channels (these are IMUs)
#last3 = raw.ch_names[-3:]
#print(f"Dropping channels: {last3}")
#raw.drop_channels(last3)

raw.plot(
    n_channels=10,     # how many channels to show at once
    scalings="auto",   # automatic scaling per channel type
    duration=10,       # seconds per window
    block=True         # keep the window open (important in scripts)
)

raw.save(f"{raw_folder}/sub-{sub}_ses-{ses}_raw.fif", overwrite=True)