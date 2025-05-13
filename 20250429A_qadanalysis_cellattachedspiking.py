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
neuron_name = '20250429A'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# cell firing kinda slowly (max.~8Hz) and irregularly (freq. going up and down all the time), then mostly
# stops to spike altogether ~5min. into recording.

# %%
block_idx = 1  # (first recording block is all tuning pulses)
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
# segment_30s_start_inms = 10000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=120,
                                                # t_start_inms=segment_30s_start_inms,
                                                plot='on')

cellattachedspikes_df = pd.DataFrame(results[0])
from singleneuron_plotting_functions import plot_cellattachedspikes_instantaneous_frequency
figure = plot_cellattachedspikes_instantaneous_frequency(cellattachedspikes_df, 20000)

# very clear from here: less than 5 minutes of recording where neuron is spiking; in these 5 minutes,
# inst.freq. goes anywhere between 0.25 - 13Hz.
