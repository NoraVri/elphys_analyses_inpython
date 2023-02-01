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
# recordings performed in 2022-05 all had low QX concentration (~0.3mM);
# recordings performed in 2022-12 were done with tip filled with QX-free intra (with varying success; in at least one case QX-containing intra could be seen to come out of the pipette before the neuron was patched).




# %% apply once: get recordingblocks_index for each neuron, updated with timestamp and events-frequencies information
for neuron in qxpatched_recordings_metadata.name:
    neuron_data = SingleNeuron(neuron)
    print(neuron)
    neuron_data.get_depolarizingevents_frequencies_byrecordingblocks()
    neuron_data.write_results()

