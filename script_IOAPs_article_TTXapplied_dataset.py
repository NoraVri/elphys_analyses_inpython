# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import singleneuron_plotting_functions as plots

path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')  # metadata on each recording
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')  # metadata on the experiment day - mouse type etc. that is the same for all neurons recorded on that day

# in this script: analysis and plotting of TTX-applied experiments
# Dataset: neurons recorded without and with TTX in the bath.

# Getting experiment-day metadata for days on which TTX was used:
ttx_experimentdays_metadata = experimentdays_metadata[experimentdays_metadata.specialchemicals_type.str.contains('TTX', na=False)]
# Getting recordings metadata for neurons recorded on those days:
ttxdays_recordings_metadata = recordings_metadata[recordings_metadata.date.isin(ttx_experimentdays_metadata.date)]




# %%
# On all experiment days where QX was applied, at least one neuron was patched without QX to see that proper APs are present.
# Getting recordings metadata for only neurons that were patched with QX in the pipette:
qxpatched_recordings_metadata = qxdays_recordings_metadata[((qxdays_recordings_metadata.elphysrecording_notes.str.contains('QX', na=False))
                                                            & (qxdays_recordings_metadata.total_t_recorded_in_s > 0))]
