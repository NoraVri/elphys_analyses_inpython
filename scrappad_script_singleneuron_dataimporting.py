# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:24:39 2020

@author: neert
"""
# %% imports
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgnl
import quantities as pq
from neo import io
from igor import packed
import re
from neo.core import Block, ChannelIndex, Segment

os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from singleneuron_class import SingleNeuron
# %%
#exampleData_pClamp = SingleNeuron("20190729A")



exampleData_SutterPatch = SingleNeuron("20200308D")
cell20200310C = SingleNeuron("20200310C")
#cell20200310G = SingleNeuron("20200310G") this one bugs out for some reason
cell20200312F = SingleNeuron("20200312F")

# %%
# os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive\\myData_nRiMLabRig")
# file_name = '20200310C.pxp'
# reader = io.IgorIO(filename=file_name)
# _, filesystem = packed.load(file_name)
# #getting the names of the subderictories that contain recorded data
# subdirectories_list = []
# for key, value in filesystem['root'][b'SutterPatch'][b'Data'].items():
#     key_converted = key.decode("utf-8")
#     result = re.search(r'R([0-9]*)_S([0-9]*)_', key_converted)
#     if result:
#         subdirectories_list.append(key_converted)
# #get the number of unique runs, and import data as one block per run
# runs_list = [item[0:3] for item in subdirectories_list]
# unique_runs = list(set(runs_list))
# unique_runs.sort()
# # %%
# run = unique_runs[0]
# traces_names = [item for item in subdirectories_list if item.startswith(run)]
#         #setting up an empty block with the right number of channel_indexes:
# block = Block()
# for i in range(len(traces_names)):
#     chidx = ChannelIndex(index=i,channel_names=['Channel Group '+str(i)])
#     block.channel_indexes.append(chidx)
# # %%
# #importing the raw analogsignals for each channel
# vtrace_name = [name for name in traces_names if 'S1' in name][0]
# itrace_name = [name for name in traces_names if 'S2' in name][0]
# if len(traces_names) == 3:
#     auxtrace_name = [name for name in traces_names if 'S3' in name][0]
#     auxsignals = reader.read_analogsignal(path='root:SutterPatch:Data:'+auxtrace_name)
# vsignals = reader.read_analogsignal(path='root:SutterPatch:Data:'+vtrace_name)
# isignals = reader.read_analogsignal(path='root:SutterPatch:Data:'+itrace_name)


