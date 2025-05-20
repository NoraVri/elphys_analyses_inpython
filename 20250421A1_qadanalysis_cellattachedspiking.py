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
neuron_name = '20250421A1'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# removing blocks where neuron isn't spiking at all:
# blockslist = neuron_data.get_blocknames(printing='off')
# neurondead_blockslist = blockslist[2:]
# for block in neurondead_blockslist:
#     neuron_data.rawdata_remove_nonrecordingblock(block)
# neuron_data.write_results()

# notes on raw data:
# Unfortunately, looks like most of this data is useless: neuron stops spiking during the second recordingblock
# and never gets back to it; and in the second block, signals are clipped at 200pA for some reason so it's
# unlikely that spikes will get picked up properly for the timeperiod where neuron is spiking fastest.

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_PT_0000
# t_start: 122000; mean freq.=19.93848837873434, CoV=4.083939710767326 (just after tuning pulses turned off)
# t_start: 125000; mean freq.=8.498766111518439, CoV=2.561127591698505 (neuron pauses for multiple seconds at the time here)

# use file gapFree_PT_0001
# t_start: 0; mean freq.=0.6321606134189105, CoV=0.7530609141293891
# t_start: 130000; mean freq.=1.122647483427794, CoV=0.7363406465422999
# t_start: 180000; mean freq.=0.9926029501885947, CoV=0.5058983212311794
# t_end: 270000; mean freq.=1.3343147002741789, CoV=1.9266205854580125