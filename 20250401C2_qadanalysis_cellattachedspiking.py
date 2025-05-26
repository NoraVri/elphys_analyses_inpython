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
neuron_name = '20250401C2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# pretty nice recording overall, with spikes pretty easy to extract from both vc and cc recordings

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 4  # the first couple of blocks are tuning pulses/VC-CCswitches
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
# t_start_inms = 5000  # after tuning pulses turned off
t_end_inms = 183000  # after this, baseline has episodes of being too unstable for easy and accurate spike extraction
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.5,
                                                tracelength_30s=False,
                                                # t_start_inms=t_start_inms,
                                                t_end_inms=t_end_inms,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# looks like a handful of spikes were missed in detection; few enough to not be of real concern for now
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0004.abf
# mean freq. = 14.18329931547667
# isi CoV = 0.15328178462855085

# %% recording condition: gabazine applied @ RT
block_idx = 23
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=40,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# spike frequency just wanders up and down broadly, this really looks like general irregularity more than any trends in speed
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_wtih_gabazine_0001.abf
# mean freq. = 17.022021647444575
# isi CoV = 0.15312650527636143

# %% recording condition: "gabazine overload" (dose of gabazine directly to bath, twice)
block_idx = 18
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 91000  # cutting off switch to cc
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=40,
                                                tracelength_30s=False,
                                                t_end_inms=t_end_inms,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# contrary to C1, I see a drop here with freq going from ~16Hz to ~12 in the first 7s; it then recovers and stays
# mostly steady until starting to climb again (with wobbles back down) towards the end of another minute of recording.
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))  # number calculated for entirety of recording marked here
print('isi CoV = ' + str(results[3]))
# recording block gapFree_wtih_gabazineOverload_0000.abf
# mean freq. = 15.511835486408415
# isi CoV = 0.15489606274143622

block_idx = 21
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=50,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# freq trends up in the first 10s, then down again a bit; does some more wobbles over the course of this minute.
# Looks like grand average should be a pretty accurate reflection of overall frequency
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_wtih_gabazineOverload_0003.abf
# mean freq. = 22.78254106281806
# isi CoV = 0.14489358102053507

# %% recording condition: gabazine and quinpirole applied
block_idx = 15
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.7,
                                                tracelength_30s=False,
                                                getbaseline_lpfilter_freq=12,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# back to the mostly just gneral irregularity, though freq does look to be clearly trending up over the last 20s of this recording
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_with_quinpirole_0000.abf
# mean freq. = 21.00522224823033
# isi CoV = 0.1518183954684868

# %% recording condition: drug washout
# these are not long recordings, there's no way drug fully washed out
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=50,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# yup, that's a practically flat freq vs time curve
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_drugsWashOut_0000.abf
# mean freq. = 22.587217415021527
# isi CoV = 0.11795836704290046