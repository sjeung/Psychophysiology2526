import mne
import os

raw_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\01_raw-data"
preprocessed_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\02_preprocessed"
os.makedirs(preprocessed_folder, exist_ok=True)

# parameters
l_freq, h_freq = 0.1, 30
resample_sfreq = 250
sub = "001"
ses = "oddballstand"

# for sub in subjects:
#    for ses in sessions:
#        print(f"Loading sub-{sub}, session-{ses}")

raw_path = os.path.join(raw_folder, f"sub-{sub}_ses-{ses}_raw.fif")
raw = mne.io.read_raw_fif(raw_path, preload=True)

# unprocessed
raw.plot(n_channels=20, duration=10, block=True)

# power spectral density
raw.plot_psd(fmax=80)

# average referencing
raw.set_eeg_reference("average")

# filtering & resampling
raw.filter(l_freq, h_freq)
raw.resample(resample_sfreq)

# now preprocessed
raw.plot(n_channels=20, duration=10, block=True)

# save output
save_path = os.path.join(preprocessed_folder, f"sub-{sub}_ses-{ses}_preprocessed.fif")
raw.save(save_path, overwrite=True)