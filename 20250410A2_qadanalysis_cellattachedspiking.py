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
neuron_name = '20250410A2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# decent recording; signal not great (especially in VC) even though nice loose seal

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)


## used gui to find spikes

# recording condition: baseline @ RT
# use file gapFree_0000
# t_start: 116000; mean freq.=17.30765360542574, CoV=0.0756757589014902 (recording file start right after tuning pulses turned off; detection threshold = 2, lpfilter=10, hpfilter=1000)
# t_end: 150000; mean freq.=17.302459397062947, CoV=0.07531552056803585

# recording condition: baseline @ PT
# use file gapFree_tempUp_0000
# t_end: 1270000; mean freq.=16.555181704848668, CoV=0.12695053996790118  (detection threshold = 50)

# recording condition: gabazine applied @ PT
# use file gapFree_tempUp_GabazineWashIn_0000
# t_end: 343000; mean freq.=20.009485233368597, CoV=0.09342930855146879 (detection threshold=40)

# use file gapFree_tempUp_withGabazine_0000
# t_start: 0; mean freq.=19.297096557511882, CoV=0.08052419024818148 (detection threshold = 40)
