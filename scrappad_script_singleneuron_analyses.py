# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:21:16 2020

@author: neert
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgnl
import quantities as pq

os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from singleneuron_class import SingleNeuron
# %% abf files
#emptycell_RawData = SingleNeuron("20190814")
rawdata_20190814A = SingleNeuron("20190814A")
cell20191119A_RawData = SingleNeuron("20191119A")
# %% plotting raw data
#this throws up a plot for each block that is read in
rawdata_20190814A.plot_allrawdata()
# %% cleanup
file_toexcept = rawdata_20190814A.rawdata_blocks[0].file_origin #in this block, there are 2 recording channels active but only Ch1 is actually recording from a neuron
rawdata_20190814A.rawdata_remove_nonrecordingchannel(file_toexcept,2)
#rawdata_20190814A.plot_block_byname(file_toexcept)
#TODO: adjust code to record which files are getting excepted, and save this information

# %% fast-events analyses
#rawdata_20190814A.get_depolarizingevents_fromRawData()
segment = rawdata_20190814A.rawdata_blocks[0].segments[0]
segment_slice = segment.time_slice(t_start=710*pq.s,t_stop=730*pq.s)
from singleneuron_analyses_functions import get_depolarizingevents

depolarizingevents_candidates = get_depolarizingevents(segment_slice)

# %%
single_voltage_trace = segment.analogsignals[0]
time_axis = single_voltage_trace.times
time_axis = time_axis.rescale('ms').magnitude
voltage_recording = np.squeeze(single_voltage_trace)

# %%
sos = sgnl.butter(10, 1000, 'lowpass', fs=20000, output='sos')
filtered = sgnl.sosfilt(sos, voltage_recording)
decimated = sgnl.decimate(voltage_recording,2)
decimated_time_axis = time_axis[::2]

filtered_decimated = sgnl.decimate(filtered,2)
sos2 = sgnl.butter(10,1000,'lowpass', fs=10000, output='sos')
decimated_filtered = sgnl.sosfilt(sos2, decimated)
plt.figure()
plt.plot(time_axis,voltage_recording,'blue')
plt.plot(time_axis, filtered, 'black')
plt.plot(decimated_time_axis,decimated,'red')
plt.plot(decimated_time_axis,decimated_filtered,'green')

# %%
sos = sgnl.butter(10, 1000, 'lowpass', fs=20000, output='sos')
filtered = sgnl.sosfilt(sos, voltage_recording)
derivative = np.diff(filtered,append=filtered[-1])

# %%

# decimate_window10 = sgnl.decimate(voltage_recording, 10)
# decimate10_time_axis = time_axis[0::10]
# plt.plot(decimate10_time_axis,decimate_window10,'red')
decimate_window4 = sgnl.decimate(voltage_recording, 4)
# decimate5_time_axis = time_axis[0::5]
# plt.plot(decimate5_time_axis,decimate_window5,'black')
# plt.plot(decimate10_time_axis,decimate_window5_2,'green')
decimate_window2 = sgnl.decimate(voltage_recording,2)
decimate2_time_axis = time_axis[::2]
decimate_window2_2 = sgnl.decimate(decimate_window2, 2)
decimate4_time_axis = time_axis[::4]
plt.plot(decimate2_time_axis,decimate_window2,'black')
plt.plot(decimate4_time_axis,decimate_window2_2,'green')
plt.plot(decimate4_time_axis,decimate_window4,'red')
plt.plot(time_axis,voltage_recording,'blue')
# %%
medfiltered = sgnl.medfilt(decimate_window2,3)
plt.figure()
plt.plot(time_axis,voltage_recording,'blue')
plt.plot(decimate2_time_axis,decimate_window2,'black')
plt.plot(decimate2_time_axis,medfiltered,'green')
# %% pxp files
cell20200310F_RawData = SingleNeuron_RawData("20200310F")
os.chdir(cell20200310F_RawData.file_path)
# %%
from neo import io
import igor
file_name = cell20200310F_RawData.file_path+'\\'+cell20200310F_RawData.name+'.pxp'
reader = io.IgorIO(filename=file_name)