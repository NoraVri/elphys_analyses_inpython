# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

# quick-and-dirty analysis steps:
# import data, cleanup where necessary (i.e., remove channels not belonging to neuron and/or any any sections recorded in the wrong mode)
# identify unique recording conditions (temperature, drug) and collect all files per condition
# per condition, pick a 30s trace to get numbers from and (manually) place these in excel table

## importing the data
neuron_name = '20250410C1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

## raw data cleanups
# # removing recording channel not belonging to this neuron:
blocknameslist = neuron_data.get_blocknames(printing='off')
for blockname in blocknameslist:
    neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# looks like seal never actually built up; no spikes recorded.
# Removing blocks and updating total time recorded to 0:
for blockname in blocknameslist:
    neuron_data.rawdata_remove_nonrecordingblock(blockname)
neuron_data.write_results()




