import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

epoched_folder = r"P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\EEG-Data\03_epoched"
sessions = ["oddballstand", "oddballwalk"]

RTs = []
SDs = []
for ses in sessions:
    csv_path = os.path.join(epoched_folder, f"sub-001_ses-{ses}_onsets.csv")
    behav_df = pd.read_csv(csv_path)
    behav_df = behav_df.apply(pd.to_numeric, errors='coerce')
    max_rt = 1.0  # maximum RT considered a hit (seconds)

    # prepare arrays
    targets = behav_df["target_onset_sec"].dropna().values
    responses = behav_df["response_onset_sec"].dropna().values
    standards = behav_df["standard_onset_sec"].dropna().values

    # ignore responses before first stimulus (standard or target)
    first_stim = min(np.min(standards), np.min(targets))
    responses = np.array([r for r in responses if r >= first_stim])

    # compute RTs
    rt_list = []
    misses = 0
    used_responses = set()

    for target_time in targets:
        # find first response after target within max_rt
        valid_resps = [r for r in responses if r >= target_time and r <= target_time + max_rt and r not in used_responses]
        if valid_resps:
            rt = valid_resps[0] - target_time
            rt_list.append(rt)
            used_responses.add(valid_resps[0])
        else:
            misses += 1  # no valid response → miss

    # compute false alarms
    false_alarms = len(responses) - len(used_responses)

    # compute stats
    mean_rt = np.mean(rt_list) if rt_list else np.nan
    sd_rt = np.std(rt_list, ddof=1) if len(rt_list) > 1 else np.nan

    # print summary
    print(f"Number of targets: {len(targets)}")
    print(f"Hits: {len(rt_list)}")
    print(f"Misses: {misses}")
    print(f"False alarms (after first stimulus): {false_alarms}")
    print(f"Mean RT: {mean_rt:.3f} s")
    print(f"SD RT: {sd_rt:.3f} s")

    RTs.append(mean_rt)
    SDs.append(sd_rt)

# Create bar plot with error bars
plt.figure(figsize=(8,5))
plt.bar(sessions, RTs, yerr=SDs, capsize=5, color='skyblue', edgecolor='none')
plt.ylabel('Reaction Time')
plt.title('Mean RTs Across Sessions')

plt.show()