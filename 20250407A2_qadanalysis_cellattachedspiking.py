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
print('recording condition: ')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

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
print('recording condition: ')
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% @ RT with glu-blockers and other drugs washed off
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

# %% @ PT with glu-blockers and other drugs washed off
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

# %% @ PT with glu-blockers and gabazine (washed on again)
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

# %% @ PT with glu-blockers and gabazine washed off again
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

# %% @ PT with glu-blockers and gabazine washed on again again
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

# %% @ PT with glu-blockers and gabazine washed off again again
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
