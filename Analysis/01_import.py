import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File path
filename = r'P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\Data\00_source-data\demo_sub-001_addition.txt'

# Count header lines (lines starting with '#') : this is common to all files
header_lines = 0
with open(filename, 'r') as f:
    for line in f:
        if line.startswith("# EndOfHeader"):
            header_lines += 1
            break
        header_lines += 1

# Load the last two columns (EDA and ECG)
data = np.loadtxt(filename, skiprows=header_lines, usecols=(-2, -1)) # -2, -1 : two last columns
eda = data[:, 0]

# Build a time axis
fs = 1000  # samples per second
t = np.arange(len(eda)) / fs # create "time" values in seconds

# Plot EDA
plt.figure()
plt.plot(t, eda)
plt.title("EDA Signal")
plt.xlabel("Time [s]")
plt.ylabel("EDA [µS]")
plt.show(block=False)

# ToDo : repeat for ECG data

# Create a DataFrame
df = pd.DataFrame({
    'time': t,
    'eda': eda
})

# Save to CSV
output_file = r'P:\Sein_Jeung\Teaching\Project Psychophysiology\Psychophysiology2526\Data\01_raw-data\raw_demo_sub-001_addition.csv'
df.to_csv(output_file, index=False)  # index=False avoids writing row numbers

print(f"CSV saved to {output_file}")

# ToDo : do this for multiple sessions