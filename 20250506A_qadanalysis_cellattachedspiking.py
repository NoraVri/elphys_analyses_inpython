# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_analyses_functions import make_cellattachedspikepeaks_dictionary
from singleneuron_plotting_functions import plot_cellattachedspikes_instantaneous_frequency
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
neuron_name = '20250506A'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## raw data cleanups
# in the first two files seal is still being tested (first one all the way, second partially (in VC; either way, sealing is going nowhere, but signal looks OK nonetheless).
# Nothing really to clean up; cell seems to die towards the end
# Note: as I'm looking more closely, it seems this neuron may be slowing down and becoming more irregular already
# during the first few minutes of recording; should definitely pay close attention though, cause S/N not great and here and there spikes won't get picked up right unless detection parameters are set carefully.
## ran gui.py to extract spike peaks

## recording condition: baseline @PT
# use file gapFree_0001
# t_start: 88000; mean freq.=9.369623209702619, CoV=0.11160353788534877 (where recording is first without seal-test pulses; detection threshold set to -50 to get all spikes picked up)
# t_end: 310000; mean freq.=4.138230699464441, CoV=0.4946829219439173 (end of this block; detection threshold still set to 50)

## recording condition: cool down to RT
# use file gapFree_tempDown_0000 - temp. down to 25.9C after ~6 minutes
# t_end: 619600; mean freq.=9.476179716928662, CoV=0.09214420061389599 (end of recording block, temp. at its lowest)
# t_start: 250000; mean freq.=4.953015624512926, CoV=0.22706914965262054 (where spiking picks back up, after having been practically off for ~2min. after ~2min. of cooling; detection threshold set to 50 to get all spikes)

## recording condition: warm back up to PT
# use file gapFree_tempUp_0000 - starting from 24.8C, temp.back up to 30degrees C after 3 minutes, according to notes
# t_start: 0, mean freq.=9.703193462473406, CoV=0.08699698751697238 (start of this recording file - temp.still low)
# t_start: 180000, mean freq.=2.4548192250377747, CoV=0.6104429809525118 (time where temp.reached 30C; also time where spiking slows down quite suddenly)

# %% comparing temperature conditions directly
block_idx = 1  # starting condition, PT
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 88000  # cutting off part of recording where tuning pulses still on
results1 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                t_start_inms=t_start_inms,
                                                 tracelength_30s=False,
                                                plot='on')
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results1[2]))
print('isi CoV = ' + str(results1[3]))
# recording block gapFree_0001.abf
# mean freq. = 7.618229496337825
# isi CoV = 0.6555462576506176

block_idx = 2  # cool down to RT
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 500000  # taking just the last ~100s, where temp. presumably at its coolest (and S/N most decent)
results2 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                t_start_inms=t_start_inms,
                                                 tracelength_30s=False,
                                                plot='on')
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results2[2]))
print('isi CoV = ' + str(results2[3]))
# recording block gapFree_tempDown_0000.abf
# mean freq. = 9.067214491483172
# isi CoV = 0.16421220175336387

block_idx = 3  # warming back up to PT
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 240000  # cell stops spiking after that anyway
results3 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                t_end_inms=t_end_inms,
                                                 tracelength_30s=False,
                                                plot='on')

results_list = [results1, results2, results3]
allresults_dict = make_cellattachedspikepeaks_dictionary()

for results in results_list:
    spikes_dict = results[0]
    for key in allresults_dict.keys():
        allresults_dict[key] += list(spikes_dict[key])
results_df = pd.DataFrame(allresults_dict)

figure2 = plot_cellattachedspikes_instantaneous_frequency(results_df, 20000)
