import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

resultsFolder = r'C:\Users\seinj\Teaching2526\Psychophysiology2526\Results'
filename = os.path.join(resultsFolder, f'ECG_results.csv')
print(f'Reading {filename}...')

# Load data
alldata = pd.read_csv(filename)
print("Loaded:", filename)
print(alldata.keys())

for col in ["ECG_Rate_Mean", "HRV_RMSSD"]:
    alldata[col] = alldata[col].apply(
        lambda x: float(eval(x)[0][0]) if "[[" in str(x) else float(x)
    )
# Key psychophysiological measures
key_features = ["ECG_Rate_Mean","HRV_RMSSD"]

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

