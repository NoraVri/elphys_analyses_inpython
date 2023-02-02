# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import singleneuron_plotting_functions as plots

path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')  # metadata on each recording
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')  # metadata on the experiment day - mouse type etc. that is the same for all neurons recorded on that day

# in this script: analysis and plotting of QX-314-applied experiments
# Dataset: neurons recorded with QX-314 in the pipette.
# Different concentrations and configurations (in some experiments, pipette tip was filled with QX-free intra to get
# a time-delayed effect); this information will have to be recovered manually per neuron from experiment-day notes.

# Getting experiment-day metadata for days on which QX-314 was used:
qx_experimentdays_metadata = experimentdays_metadata[experimentdays_metadata.specialchemicals_type.str.contains('QX-314', na=False)]
# Getting recordings metadata for neurons recorded on those days:
qxdays_recordings_metadata = recordings_metadata[recordings_metadata.date.isin(qx_experimentdays_metadata.date)]
# On all experiment days where QX was applied, at least one neuron was patched without QX to see that proper APs are present.
# Getting recordings metadata for only neurons that were patched with QX in the pipette:
qxpatched_recordings_metadata = qxdays_recordings_metadata[((qxdays_recordings_metadata.elphysrecording_notes.str.contains('QX', na=False))
                                                            & (qxdays_recordings_metadata.total_t_recorded_in_s > 0))]
# Recordings performed in 2022-05 all had low QX concentration (~0.3mM);
# Recordings performed in 2022-12 were done with tip filled with QX-free intra (with varying success; in some cases
# QX-containing intra could be seen to come out of the pipette before the neuron was patched; in other cases neurons
# died before QX-containing intra reached them).
# Experiment-day notes on neurons where I attempted patching with QX-free intra in the tip of the pipette:
# 20221227C - died before QX-intra could be seen to reach the recorded neuron
# 20221227D - died while stimulating electrode was moving around; not sure whether QX reached the neuron
# 20221227E - QX-intra could be seen coming out of the pipette faintly just before patching the neuron; neuron was filled with QX-intra within 15 minutes from establishing patch
# 20221227F - QX-intra could be seen coming out of the pipette clearly before patching the neuron
# 20221227G - soma faintly labeled in QX-color by the time neuron died quickly and suddenly (~15 minutes after establishing patch); however, the last 8 sweeps of recorded data had to be excluded, and it seems that in the 5 minutes before that the neuron was able to make Na-spikes throughout..
# 20221229C - soma labeled in QX-color by file electricalStim#5
# 20221229D - both colors could be seen to come out of the pipette before patching; neuron labeled in both colors by file GapFree#1
# 20221229E - it took at least ~10 minutes for QX-intra to reach the recorded neuron
# 20221229F - died after ~5min. of recording, no visible fluorescent labeling in either color

# Based on these notes, neurons 20221227C, 20221227D, 20221227G and 20221229F should be excluded from the QX-patched dataset
# because QX (probably) did not actually reach the recorded neurons.
to_drop = ['20221227C', '20221227D', '20221227G', '20221229F']
qxpatched_recordings_metadata = qxpatched_recordings_metadata[~qxpatched_recordings_metadata.name.isin(to_drop)]

