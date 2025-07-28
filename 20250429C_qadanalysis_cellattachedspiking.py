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
neuron_name = '20250429C'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# starts off as a plenty nice recording with signal >100pA above noise, but deteriorating and totally gone by
# ~190s into gapFree_gabazineWashIn (just as drug solution is supposed to hit the bath).

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_0002
# t_start: 107000; mean freq.=38.89769805160629, CoV=0.1142529281602722 (start of recording, where tuning pulses first turned off)
# t_start: 250000; mean freq.=41.11361061065418, CoV=0.14086602294023176 (random piece from somewhere in the middle)
# t_end: 495900; mean freq.=41.890422417398575, CoV=0.1685695732253434 (end of this block)

# use file gapFree_gabazineWashIn_0000
# t_start: 0; mean freq.=41.06934001670843, CoV=0.1558378812631731 (start of this file, definitely no gabazine in the bath yet)

