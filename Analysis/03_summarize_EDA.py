import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
filename = os.path.join(resultsFolder, f'EDA_results.csv')
print(f'Reading {filename}...')

# Load data
alldata = pd.read_csv(filename)
print("Loaded:", filename)
print(alldata.keys())

# Key psychophysiological measures
key_features = ["tonic"]

# subject specific line plot
plt.figure(figsize=(8, 4))

for subj in alldata["Subject"].unique():
    sub_df = alldata[alldata["Subject"] == subj]
    plt.plot(sub_df["Session"], sub_df["tonic"], marker="o", label=subj)

plt.title(f"Tonic EDA Across Sessions")
plt.xlabel("Session")
plt.ylabel("Tonic EDA (μS)")
plt.legend()
plt.tight_layout()
plt.show()

# Normalisation
alldata["tonic_Norm,"] = None   # create empty column

# Process each subject separately
for subject_id, subject_data in alldata.groupby("Subject"):

    # Find the subject's baseline value
    baseline_value = subject_data.loc[
     subject_data["Session"] == "baseline", "tonic"
    ].values[0]

    # Compute normalized values for ALL that subject's sessions
    normalized_values = subject_data["tonic"]*100 / baseline_value

    # Save back to the main DataFrame
    alldata.loc[subject_data.index, "tonic_Norm"] = normalized_values

# plot
plot_data = alldata[alldata["Session"].isin(["addition", "subtract"])]
plt.figure(figsize=(7, 4))
plt.title("Normalized tonic EDA")
plt.xlabel("Session")
plt.ylabel("Normalized SCL in %")

# Bar plot (mean per session)
sns.barplot(
    data=plot_data,
    x="Session",
    y="tonic_Norm",
    color="lightgray",
    width=0.3
)

# Dot plot (each subject)
sns.stripplot(
    data=plot_data,
    x="Session",
    y="tonic_Norm",
    hue="Subject",
    dodge=True,
    alpha=0.8
)

plt.legend(title="Subject", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.ylim(70,160)
plt.show()