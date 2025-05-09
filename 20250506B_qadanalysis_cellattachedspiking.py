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
neuron_name = '20250506B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()
neuron_data.plot_rawdatablocks()

## raw data cleanups
# Nothing really to clean up; looks like this was quite a nice recording except baseline firing rate being too low for this to be a GABAergic neuron.
## ran gui.py to extract spike peaks

## recording condition: baseline @PT
# use file gapFree_001
# t_start: 135000ms; mean freq.=3.428897990284785, CoV=0.08215302358727657 (start of recording post seal-formation)
# t_end: 328000ms; mean freq.=2.749282609069196, CoV=0.08418957920965056 (end of recording in this condition)
# seems neuron slows down pretty suddenly ~150s into this file; after that, steady freq.~2.7Hz

## recording condition: cool down to RT
# use file gapFree_tempDown_0000, towards end of recording (where cooldown actually in effect)
# t_end: 479000ms, mean freq.=1.7190841140840323, CoV=0.09194846078975814
# mean freq. and CoV at the beginning of this file is comparable to baseline;
# in the middle (~125 - 275s into this file) neuron goes pretty quiet for quite a while (mean freq.<0.5Hz, CoV>1)

## recording condition: warm back up to PT
# use file gapFree_tempUp_0000, towards end of recording (where warmup actually in effect)
# t_end: 245000ms, mean freq.=2.7833105739708275, CoV=0.09096386505159104
# seems speedup happens starting ~30s into this recording, over the course of about 30s.

# recording condition: PT with gabazine washed on
# file gapFree_gabazineWashOn: freq.~2.6Hz at the start, 2.96Hz towards the end
# use file gapFree_gabazineApplied_0000
# t_start: 0ms, mean freq.=2.877593084069056, CoV=0.050852132193973214
# t_end: 307000ms, mean freq.=2.7092185447724075, CoV=0.0759684267863682

