# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

# importing the data
neuron_name = '20250407A1'
neuron_data = SingleNeuron(neuron_name)
# quick-and-dirty overview of data and automatically extracted spiking:
neuron_data.get_spikes_fromcellattachedrecording()
neuron_data.plot_rawdatatraces_with_cellattachedspikes()

# %% applying data cleanups
# # removing the recording channel not belonging to this neuron
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# # removing parts of the recording that do not register the neuron's behavior properly and/or muck up spike detection for some reason:
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                trace_end_t=56.5)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_GluBlockers_WashIn_0000.abf',
#                                                trace_end_t=226.6)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_with_GluBlockers_gabazineWashOn_0000.abf',
#                                                trace_end_t=305)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_0000.abf',
#                                                trace_end_t=151.9)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_with_GluBlockers_with_gabazine_with_quinpirole_0000.abf',
#                                                trace_end_t=135.5)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection

neuron_data.get_spikes_fromcellattachedrecording()
neuron_data.plot_rawdatatraces_with_cellattachedspikes()
# %% for each drug/temperature condition, find 30s where spikes were picked up cleanly
# get ISI means and stds


# baseline @ RT

# baseline @ RT with glu-blockers

# @ RT with glu-blockers and gabazine

# @ RT with glu-blockers and gabazine and quinpirole

# @ RT with glu-blockers and other drugs washed off

# @ PT with glu-blockers and other drugs washed off

# @ PT with glu-blockers and gabazine (washed on again)

# @ PT with glu-blockers and gabazine washed off again

# @ PT with glu-blockers and gabazine washed on again again

# @ PT with glu-blockers and gabazine washed off again again


# calculate: difference between with/without gabazine conditions

