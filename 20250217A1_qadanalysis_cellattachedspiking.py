# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_plotting_functions import qad_scatter_isis_fromdict
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
neuron_name = '20250217A1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# looks very nice and usable all throughout, at least by eye; massive signal initially (>1nA) but goes down pretty soon to ~150pA - S/N looking decent throughout though

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 0
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_t_start_inms = 81000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=100,  # have to set threshold closer to peaks, otherwise many of them get picked up twice (spikes all seem to have a double up-stroke)
                                                t_start_inms=segment_t_start_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
#
block_idx = 1
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_t_end_inms = 191600
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=75,  # have to set threshold closer to peaks, otherwise many of them get picked up twice (spikes all seem to have a double up-stroke)
                                                t_end_inms=segment_t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

block_idx = 1
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_t_start_inms = 285200  # for a section where applied current ~0pA  (~+200 - +1500pA before that)
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=75,  # have to set threshold closer to peaks, otherwise many of them get picked up twice (spikes all seem to have a double up-stroke)
                                                t_start_inms=segment_t_start_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole wash in
block_idx = 4
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_t_start_inms=200
segment_t_end_inms = 245000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=50,
                                                t_start_inms=segment_t_start_inms,
                                                t_end_inms=segment_t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: with quinpirole
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=55,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: with quinpirole, gabazine wash in
block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=55,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: with quinpirole and gabazine
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=55,
                                                # t_start_inms=segment_t_start_inms,
                                                # t_end_inms=segment_t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: drugs washout
block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_t_start_inms=500000  # washing in progress for ~10min.
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=55,
                                                t_start_inms=segment_t_start_inms,
                                                # t_end_inms=segment_t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))