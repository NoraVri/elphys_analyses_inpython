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
neuron_name = '20250428B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.plot_rawdatablocks()

## notes on raw data
# decent enough recording at first, but cell stops spiking after ~10 minutes.

# %% recording condition: baseline @ PT
block_idx = 0
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_30s_start_inms = 59100  # just after tuning pulses off and holding V set to 0
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=75,  # have to set threshold closer to peaks, otherwise many of them get picked up twice (spikes all seem to have a double up-stroke)
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('recording condition: baseline @ PT')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# mean freq. = 4.424086085908945
# isi CoV = 0.16873849756449005

block_idx = 1
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_30s_start_inms = 0  # start of the file
results2 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=100,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('t_start: 0s')
print('mean freq. = ' + str(results2[2]))
print('isi CoV = ' + str(results2[3]))
# mean freq. = 3.2970599498228688
# isi CoV = 0.2691236938890019

segment_30s_start_inms = 95000  # start of the file (holding V=1, current ~+75pA)
results3 = get_spikes_from_cellattachedrecording(segment, (segment_file_origin + ' part 2'), 0,
                                                detection_threshold=100,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('t_start: 95s')
print('mean freq. = ' + str(results3[2]))
print('isi CoV = ' + str(results3[3]))
# mean freq. = 3.1662305850915766
# isi CoV = 0.3354206830815836

segment_30s_start_inms = 145000  # start of the file (holding V=0, current ~0pA)
results4 = get_spikes_from_cellattachedrecording(segment, (segment_file_origin + ' part 3'), 0,
                                                detection_threshold=100,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('t_start: 145s')
print('mean freq. = ' + str(results4[2]))
print('isi CoV = ' + str(results4[3]))
# mean freq. = 2.6047002684577767
# isi CoV = 0.4229022265706242

segment_30s_start_inms = 180000  # where neuron picks back up after a clear pause
results5 = get_spikes_from_cellattachedrecording(segment, (segment_file_origin + ' part 4'), 0,
                                                detection_threshold=100,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('t_start: 180s')
print('mean freq. = ' + str(results5[2]))
print('isi CoV = ' + str(results5[3]))
# mean freq. = 2.02285829877617
# isi CoV = 0.6978063118215212


results_list = [results, results2, results3, results4, results5]
from singleneuron_analyses_functions import make_cellattachedspikepeaks_dictionary
allresults_dict = make_cellattachedspikepeaks_dictionary()

for results in results_list:
    spikes_dict = results[0]
    for key in allresults_dict.keys():
        allresults_dict[key] += list(spikes_dict[key])
results_df = pd.DataFrame(allresults_dict)

from singleneuron_plotting_functions import plot_cellattachedspikes_instantaneous_frequency
figure = plot_cellattachedspikes_instantaneous_frequency(results_df, 20000)

# OK so basically, that was just a very long way of showing that the frequencies are gradually trending down.
# Still, I think it's pretty cool to see how ISIs become more and more irregular, and the neuron speed up for a bit first before petering out

