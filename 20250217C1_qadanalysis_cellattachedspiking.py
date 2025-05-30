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
neuron_name = '20250217C1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
#

# raw data cleanups
# removing recording channel not belonging to this neuron:
# neuron_data.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 0
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start = 72000  # tuning pulses are on throughout this block; after 72s seal tight enough for this to be no longer visible in the current recording
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=50,
                                                t_start_inms=t_start,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0000.abf
# mean freq. = 11.206309577848385
# isi CoV = 0.12879518819899624

block_idx = 2
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                detection_threshold=50,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0002.abf
# mean freq. = 10.576053767292702
# isi CoV = 0.06896778413994353

# %% recording condition: quinpirole wash in
block_idx = 4
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                detection_threshold=50,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# looks like some speeding up is starting to happen right as quinpirole supposed to hit the bath
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole applied
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                detection_threshold=50,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_quinpirole_0000.abf
# mean freq. = 13.70144888968385
# isi CoV = 0.11513726273231842

# %% recording condition: quinpirole applied, gabazine wash in
block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                detection_threshold=50,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# perhaps a slight trend up, if I squint my eyes right
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole and gabazine applied
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                detection_threshold=50,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)

print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_quinpirole_gabazine_0000.abf
# mean freq. = 14.961332081014428
# isi CoV = 0.059059051915497575

# %% recording condition: drugs wash out
block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                detection_threshold=50,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# don't really see anything systematic happening to spiking freq in these 9.5min
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_drugsWashOut_0000.abf
# mean freq. = 14.886500012767153
# isi CoV = 0.14510084988535815