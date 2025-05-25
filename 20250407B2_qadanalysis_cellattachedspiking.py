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
# import data, cleanup where necessary (i.e., remove channels not belonging to neuron and/or any blocks where neuron not actually alive)
# identify unique recording conditions (temperature, drug) and collect all files per condition
# per condition, pick a 30s trace to get numbers from and (manually) place these in excel table

## importing the data
neuron_name = '20250407B2'
neuron_data = SingleNeuron(neuron_name)

## raw data cleanups
# removing recording channel not belonging to this neuron:
blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)

neuron_data.plot_rawdatablocks()
# notes on raw data:
# looks nice enough, except that neuron pauses for seconds on end once PT is reached; and then it leaves quickly and suddenly ~10min. after glu-blockers washed in

neuron_data.write_results()

# %%
# use gui.py to find spikes

# recording condition: baseline @ RT
# use file gapFree_0000
# t_start: 0; mean freq.=6.5731962675087585, CoV=0.14918392348692192
# t_end: 60000; mean freq.=6.302617110927754, CoV=0.13433236973986462

# recording condition: baseline @ PT
# use file gapFree_tempUp_0001 (cell starts to take very long pauses in spiking from the middle of this block)
# t_start: 60000: mean freq.=1.5572951682068703, CoV=1.3574018832439434
# t_start: 100000: mean freq.=0.8509551972088668, CoV=1.0272941413727432

# recording condition: glu-blockers @ PT
# use file gapFree_tempUp_gluBlockersWashIn_0000
# t_end: 310000; mean freq.=1.2709881547755462, CoV=0.750732017822529
# t_start: 420000; mean freq.=2.1196890579205117, CoV=1.4372357226967036

