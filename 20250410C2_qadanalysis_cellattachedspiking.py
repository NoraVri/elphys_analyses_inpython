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
neuron_name = '20250410C2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

## raw data cleanups
# # removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

# notes on raw data:
# slow-spiking neuron (freq. max 2Hz, by eye) and does lots of pauses of multiple seconds at the time.

## used gui to find spikes

# recording condition: baseline @ RT
# use file gapFree_RT_0000 (whole file; just under 160s)
# mean freq.=0.49412917010329, CoV=1.5219288817762353

# recording condition: temp. increase to PT
# use file gapFree_tempUp_0000 (whole file; by the time temp. is actually up spiking is gone).
# mean freq.=0.5665454888815447, CoV=1.643038688751138
