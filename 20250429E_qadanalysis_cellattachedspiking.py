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
neuron_name = '20250429E'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# cell was spiking intermittently while getting attached, but no longer by the time seal formation done
# I did see a short stretch at t=27s into gapFree_0000 where cell fires 8 spikes in 400ms (-->freq.20Hz)

# no point in trying to extract spikes, there's way too few of them anyway

