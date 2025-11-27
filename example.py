import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

# follow https://neuropsychology.github.io/NeuroKit/introduction.html
# Generate synthetic signals
ecg = nk.ecg_simulate(duration=15, heart_rate=60)
ppg = nk.ppg_simulate(duration=15, heart_rate=70)
rsp = nk.rsp_simulate(duration=15, respiratory_rate=15)
eda = nk.eda_simulate(duration=15, scr_number=3)
emg = nk.emg_simulate(duration=15, burst_number=2)

# Visualise biosignals
data = pd.DataFrame({"ECG": ecg,
                     "PPG": ppg,
                     "RSP": rsp,
                     "EDA": eda,
                     "EMG": emg})
nk.signal_plot(data, subplots=True)
plt.show()