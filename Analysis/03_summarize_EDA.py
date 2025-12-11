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
for feat in key_features:
    plt.figure(figsize=(8, 4))

    for subj in alldata["Subject"].unique():
        sub_df = alldata[alldata["Subject"] == subj]
        plt.plot(sub_df["Session"], sub_df[feat], marker="o", label=subj)

    plt.title(f"{feat} Across Sessions")
    plt.xlabel("Session")
    plt.ylabel(feat)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Normalisation
# Normalized_value = value / subject's_baseline_value
# So baseline becomes 1.0 for everyone.

#for feature in key_features:

 #   norm_col = feature + "_Norm"
 #   alldata[norm_col] = None   # create empty column

    # Process each subject separately
 #   for subject_id, subject_data in alldata.groupby("Subject"):

        # Find the subject's baseline value
  #      baseline_value = subject_data.loc[
   #         subject_data["Session"] == "baseline", feature
   #     ].values[0]

        # Compute normalized values for ALL that subject's sessions
    #    normalized_values = subject_data[feature] / baseline_value

        # Save back to the main DataFrame
     #   alldata.loc[subject_data.index, norm_col] = normalized_values

#print("\nAdded baseline-normalized columns:")
#print([f + "_Norm" for f in key_features], "\n")


plot_data = alldata[alldata["Session"].isin(["Addition", "Subtraction"])]

#  BAR PLOTS WITH NORMALIZED VALUES
for feature in key_features:

    # only select addition / subtract sessions
    plot_data = alldata[alldata["Session"].isin(["addition", "subtract"])]
    norm_col = feature + "_Norm"

    plt.figure(figsize=(7, 4))
    plt.title(f"{feature} by Session (Normalized to Baseline)")
    plt.xlabel("Session")
    plt.ylabel("Normalized Value (Baseline = 1.0)")

    # Bar plot (mean per session)
    sns.barplot(
        data=plot_data,
        x="Session",
        y=norm_col,
        color="lightgray"
    )

    # Dot plot (each subject)
    sns.stripplot(
        data=plot_data,
        x="Session",
        y=norm_col,
        hue="Subject",
        dodge=True,
        alpha=0.8
    )

    #plt.axhline(1.0, color="black", linestyle="--")
    plt.legend(title="Subject", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()