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
neuron_name = '20250407A2'
neuron_data = SingleNeuron(neuron_name)

## raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

# %% going over recording conditions individually:
# empty code block for copy-pasting
# neuron_data.plot_rawdatablocks()
# #
# block_idx =
# segment = neuron_data.blocks[block_idx].segments[0]
# segment_file_origin = neuron_data.blocks[block_idx].file_origin
# segment_30s_start_inms = None
# segment_30s_end_inms = None
# results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
#                                                 # detection_threshold=None,
#                                                 # getbaseline_lpfilter_freq=0.5,
#                                                 # getnoise_hpfilterfreq=5000,
#                                                 t_start_inms=segment_30s_start_inms,
#                                                 t_end_inms=segment_30s_end_inms,
#                                                 plot='on')
# print('recording condition: ')
# print('mean freq. = ' + str(results[2]))
# print('isi CoV = ' + str(results[3]))

# %% recording condition: baseline @ RT
# neuron_data.plot_rawdatablocks('gapFree_0')
# let's just take the first file cause why not; 30s just post seal forming
block_idx = 0
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_30s_start_inms = 10000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.25,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('recording condition: baseline @ RT')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# mean freq. = 19.416889675848605
# isi CoV = 0.05297397605762597

# %% recording condition: baseline with glu-blockers @ RT
# neuron_data.plot_rawdatablocks('gapFree_GluBlockers')
# let's take the final file in this condition, to be sure that blockers took effect
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_30s_start_inms = 0
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.25,
                                                # getbaseline_lpfilter_freq=0.5,
                                                # getnoise_hpfilterfreq=5000,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('recording condition: baseline with glu-blockers @ RT')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# mean freq. = 19.455742379135394
# isi CoV = 0.048800849134231265

# %% recording condition: glu-blockers and gabazine @ RT
# neuron_data.plot_rawdatablocks('Blockers_with_gabazine_0')
# exactly one block in this condition; let's take it from the start
block_idx = 21
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_30s_start_inms = 0
segment_30s_end_inms = None
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.25,
                                                # getbaseline_lpfilter_freq=0.5,
                                                # getnoise_hpfilterfreq=5000,
                                                t_start_inms=segment_30s_start_inms,
                                                plot='on')
print('recording condition: RT with glu-block and gabazine')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# mean freq. = 19.053168049611905
# isi CoV = 0.04954040684304817

# %% @ RT with glu-blockers and gabazine and quinpirole
# neuron_data.plot_rawdatablocks('gabazine_with_quinpirole_0')
# taking the one block that's long enough and recorded in cc (less interfering artefacts that way):
block_idx = 23
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
segment_30s_start_inms = 0
segment_30s_end_inms = None
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=.25,
                                                # getbaseline_lpfilter_freq=0.5,
                                                # getnoise_hpfilterfreq=5000,
                                                t_start_inms=segment_30s_start_inms,
                                                t_end_inms=segment_30s_end_inms,
                                                plot='on')
print('recording condition: with_GluBlockers_with_gabazine_with_quinpirole')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% @ RT with glu-blockers and other drugs washed off
## use gui.py to detect spikes

# use file gapFree_with_GluBlockers_otherdrugsWashOut_0001.abf
# t_start: 100; mean freq.=20.70722893382901, CoV=0.058416379472712956
# t_end: 705000; mean freq.=20.180959281651543, CoV=0.073083196336888


# %% @ PT with glu-blockers and other drugs washed off
## use gui.py to detect spikes

# use file gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_0003.abf
# t_start: 0; mean freq.=11.582199102716261, CoV=0.1300147047262907
# t_end: 234000; mean freq.=7.534623792517405, CoV=0.18405421879565764


# %% @ PT with glu-blockers and gabazine (washed on again)
## use gui.py to detect spikes

# use file gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_with_gabazine_0000.abf
# t_start: 0; mean freq.=11.41096021055062; CoV=0.16075407892351676
# t_end: 510000; mean freq.=11.425172679723856, CoV=0.1571213947220336


# %% @ PT with glu-blockers and gabazine washed off again
## use gui.py to detect spikes

# use file gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashOut_0000.abf
# t_start: 0; mean freq.=7.82487128592653; CoV=0.2565642704278419 (gabazine still in effect)
# t_end: 1351000; mean freq.=14.640206843289347, CoV=0.08378842388554827  (detection threshold = 0.2)



# %% @ PT with glu-blockers and gabazine washed on again again
## use gui.py to detect spikes

# use file gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashInAgain_0000.abf
# t_start: ; mean freq.=16.63514039253565; CoV=0.0787722598723838
# t_end: 683000; mean freq.=23.60693943564348, CoV=0.056527561451367725


# %% @ PT with glu-blockers and gabazine washed off again again
## use gui.py to detect spikes

# use file gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashOutAgain_0000.abf
# t_start: ; mean freq.=25.14556637793351; CoV=0.1778063887581394
# t_end: 1305000; mean freq.=16.929833383619968, CoV=0.10270413696999167