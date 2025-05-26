# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_plotting_functions import qad_scatter_isis_fromdict
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
neuron_name = '20250401A2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# looks very nice and usable all throughout, at least by eye; pretty big signal initially (~400pA) but goes down pretty soon to ~100pA - S/N looking decent throughout though

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 2  # the first two blocks are tuning pulses/switches between VC and CC
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=300,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
#
block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 308000  # up until change in holding V (till here, baseline holding ~+200pA)
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                t_end_inms=t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

t_start_inms = 317000  # once holdingV such that holding current ~0pA
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=100,
                                                t_start_inms=t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# from this, it looks like spike frequency may be trending one way or another; but no, it just wanders:
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)

# %% recording condition: gabazine wash in
block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=75,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# that looks like frequency is trending up:
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)

# %% recording condition: gabazine applied
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=75,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# that kinda looks like frequency is trending down again over the course of 5 min. in this condition:
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)

# %% recording condition: gabazine applied, quinpirole wash in
block_idx = 8
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 63600  # after tuning pulses turned off again
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=60,
                                                tracelength_30s=False,
                                                t_start_inms=t_start_inms,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# looks like frequency is trending up all throughout this:
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)

# %% recording condition: gabazine and quinpirole applied
block_idx = 9
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: washout
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
# t_start_inms = 330000   # this way we get the last ~100s of almost 15 minutes washing
# t_start_inms = 340000  # in those 10s things seem to have really slowed down
t_start_inms = 399000  # post tuning pulses
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                t_start_inms=t_start_inms,
                                                tracelength_30s=False,
                                                detection_threshold=40,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))