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
neuron_name = '20250506C'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## raw data cleanups
# Nothing really to clean up, though looks like not a good recording: spiking barely visible (if at all) by the time gabazine washing in
## ran gui.py to look at extracted peaks
# yes it's quite clear from here, this cell is not happy for long:
# it's spiking very steadily at first (mean freq.=43.69, CoV=0.1356), but speeds up and becomes more irregular such that
# 2 minutes later freq.=52.93 and CoV=0.2579 (before any drug applied).
# By the time drug gets washed on spiking is highly intermittent, if at all visible.

