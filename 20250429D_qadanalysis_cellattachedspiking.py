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
neuron_name = '20250429D'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# from recording day: same slices as previous cell, decided to start from condition with gabazine still on
# closed circulation loop after 25min. of washing then went to have lunch; 40min. later cell still there (S/N got worse but looks still OK).
# Data mostly very nice, spikes are >100pA above detection threshold for much of it

# recording condition: gabazine @ PT
# use file gapFree_with_gabazine_0002
# t_start: 0; mean freq.=30.729979117658363, CoV=0.0769507661060932 (first 30s of this file; ~-300pA baseline applied to keep V)
# t_start: 57000; mean freq.=30.053471109053316, CoV=0.08322933975921595 (first 30s once holding V changes so that ~0pA applied)
# t_end: 286000; mean freq.=28.708998497629356, CoV=0.07513234765102703 (last 30s)

# recording condition: baseline with gabazine washed off @ PT
# use file gabazineWashOff_0000
# t_start: 0; mean freq.=28.40861616617369, CoV=0.08270191247390357 (start of this file; should be comparable to baseline (above))
# t_start: 1200000; mean freq.=30.24873224685504, CoV=0.08074092577073878 (the 20min. mark)
# t_start: 1800000; mean freq.=29.639976207820634, CoV=0.08347173293150507 (30 min.)
# t_start: 2300000; mean freq.=30.45951742896328, CoV=0.09437065363400214 (just under 40min.)
# t_end: 2406000; mean freq.=30.54645704592684, CoV=0.09223984982049409 (end of the recording file)

# recording condition: cool down to RT
# use file gapFree_gabazineWashOff_tempDown_0000
# t_start: 0; mean freq.=31.154522419890757, CoV=0.09321309024898919
# t_start: 120000; mean freq.=28.394458899940474, CoV=0.1006922741605139
# t_start: 180000; mean freq.=26.341156467138838, CoV=0.09275053896437081
# t_end: 2440000; mean freq.=23.60994363753895, CoV=0.12488191103470257 (last 30s; detection threshold set to 50 to ensure all spikes get picked up (I saw one noisy spike get picked up as two, but no mistakes otherwise))

