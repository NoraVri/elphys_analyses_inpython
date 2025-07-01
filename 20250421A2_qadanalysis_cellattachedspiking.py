# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_plotting_functions import plot_cellattachedspikes_instantaneous_frequency
from singleneuron_analyses_functions import make_cellattachedspikepeaks_dictionary
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
neuron_name = '20250421A2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# probably a DAergic neuron: manual count got as high as 6spikes/s but never more.
# Lots of conditions recorded, but doesn't look like there's any effect that is attributable to manipulations.

## raw data cleanups
# # removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# # removing the final recordingblock where neuron no longer spiking:
# neuron_data.rawdata_remove_nonrecordingblock('gapFree_tempUp_gabazineWashOff_0001.abf')
# neuron_data.write_results()

## used gui to find spikes

# recording condition: baseline @ PT
# use file gapFree_PT_0000; threshold set to 1 to catch spikes cleanly from CC data
# t_start: 103000; mean freq.=4.76045330474778, CoV=0.4839516913430591 (just after tuning pulses turned off)
# t_end: 167000; mean freq.=1.8432795072531287, CoV=0.4692887526827862 (end of recording, before switching to VC)

# use file gapFree_PT_0001
# t_start: 0; mean freq.=2.4574744431310993, CoV=0.2221611386700212 (recording file start)
# t_end: 332000; mean freq.=2.4553922662060206, CoV=0.09108267074060024 (recording file end)



# %% @PT, comparing gabazine conditions (before, wash-on, applied, wash-off)
block_idx = 1
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                plot='on')

block_idx = 2
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results1 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                plot='on')

block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results2 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                plot='on')

block_idx = 4
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results3 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                getnoise_hpfilterfreq=3000,
                                                detection_threshold=60,
                                                plot='on')

block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results4 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                plot='on')

results_list = [results, results1, results2, results3, results4]
allresults_dict = make_cellattachedspikepeaks_dictionary()

for results in results_list:
    spikes_dict = results[0]
    for key in allresults_dict.keys():
        allresults_dict[key] += list(spikes_dict[key])
results_df = pd.DataFrame(allresults_dict)

figure = plot_cellattachedspikes_instantaneous_frequency(results_df, 20000)

# seems like neuron may slow down slightly with gabazine application; but then it slows down more with gabazine washoff,
# so that could easily be an artefact of the neuron slowing down overall w/o there being any gabazine effect

# %% comparing PT and RT conditions
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results4 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                plot='on')
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results4[2]))
print('isi CoV = ' + str(results4[3]))
# recording block gapFree_PT_with_gabazine_0000.abf
# mean freq. = 2.1735967184633984
# isi CoV = 0.17137057816120158

block_idx = 4
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results1 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                getnoise_hpfilterfreq=3000,
                                                detection_threshold=60,
                                                plot='on')
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results1[2]))
print('isi CoV = ' + str(results1[3]))
# recording block gapFree_PT_gabazineWashOff_0000.abf
# mean freq. = 1.3761967290039165
# isi CoV = 0.5828689411165499

block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results2 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                getnoise_hpfilterfreq=1000,
                                                detection_threshold=50,
                                                plot='on')
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results2[2]))
print('isi CoV = ' + str(results2[3]))
# recording block gapFree_RT_gabazineWashOff_0000.abf
# mean freq. = 5.266582732171857
# isi CoV = 0.08089025926239171

block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 272000  # cutting off switch to CC mode
results3 = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                getnoise_hpfilterfreq=2000,
                                                 t_end_inms=t_end_inms,
                                                 tracelength_30s=False,
                                                plot='on')

results_list = [results1, results2, results3, results4]
allresults_dict = make_cellattachedspikepeaks_dictionary()

for results in results_list:
    spikes_dict = results[0]
    for key in allresults_dict.keys():
        allresults_dict[key] += list(spikes_dict[key])
results_df = pd.DataFrame(allresults_dict)

figure2 = plot_cellattachedspikes_instantaneous_frequency(results_df, 20000)

# So, clearly in these recordings the neuron's spiking frequency peters out to 0Hz once temperature turned back up.
# Still, from plotting inst.freq vs time it just looks so obvious that freq goes down when temperature goes up, and I
# think the recordings are plenty long to say that with certainty, so I'm gonna say these numbers are good.
# That does leave the question: how come spiking isn't faster at PT with gabazine?