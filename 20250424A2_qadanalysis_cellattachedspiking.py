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
neuron_name = '20250424A2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# raw data cleanup:
# removing recording channel not belonging to this neuron:
blocknameslist = neuron_data.get_blocknames(printing='off')
for blockname in blocknameslist:
    neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
neuron_data.write_results()

## notes on raw data
# recording day notes: definitely a spiking cell, but very irregular and only slowing down.
# ceased spiking within the first 5 minutes; then came back on, but ever more irregular

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_0002
# t_start: 0; mean freq.=6.422920747547268, CoV=0.4168468198350711
# t_start: 100000; mean freq.=2.054650272840433, CoV=0.6565806172160362 (where spiking can be seen to slow down significantly by eye)
# t_start: 150000; mean freq.=3.3073215395407707, CoV=0.5335288607857569 (back on for another bout of faster spiking)