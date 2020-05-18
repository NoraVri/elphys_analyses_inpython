import os
import re
import numpy as np
import quantities as pq
import matplotlib.pyplot as plt
import pandas as pd

from singleneuron_class import SingleNeuron
import singleneuron_analyses_functions as snafs
from neo.core import Block, ChannelIndex, Segment, AnalogSignal

# %%
cell20160829D = SingleNeuron('20160829D')


# %%
path = "D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\olive\myData_YaromLabRig\\20160829\\160829A"
os.chdir(path)
fileslist_txt = [file for file in os.listdir() if file.endswith('.txt')]

trigin_files = [file for file in fileslist_txt if '_' not in file]
dumperfiles = [file for file in fileslist_txt if '_' in file]

# %%
a_trigin_file = trigin_files[-1]
trigin_file_data = pd.read_table(a_trigin_file, header=None)

sampling_interval = trigin_file_data.iloc[0,1] * pq.s
currentsignals_list = []
voltagesignals_list = []
for i in range(1, len(trigin_file_data), 4):
    current_analogsignal = AnalogSignal(trigin_file_data.iloc[i,:], units=pq.nA,
                                        sampling_period=sampling_interval)
    current_analogsignal = current_analogsignal.rescale('pA')
    voltage_analogsignal = AnalogSignal(trigin_file_data.iloc[i+1,:], units=pq.mV,
                                        sampling_period=sampling_interval)
    currentsignals_list.append(current_analogsignal)
    voltagesignals_list.append(voltage_analogsignal)

voltage_analogsignal = voltagesignals_list[2]
current_analogsignal = currentsignals_list[2]
figure,axes = plt.subplots(2,1,sharex='all')
axes[0].plot(voltage_analogsignal.times,np.array(voltage_analogsignal))
axes[1].plot(current_analogsignal.times,np.array(current_analogsignal))

# %%
a_dumper_file = dumperfiles[0]
with open(a_dumper_file, 'r') as file:
    recording_channels = file.readline()
    time_metadata = file.readline()
sampling_interval = float(re.split('\t', time_metadata)[0]) * pq.ms
dumper_file_data = pd.read_table(a_dumper_file, header=None, skiprows=2)
voltage_analogsignal = AnalogSignal(dumper_file_data.iloc[:,0], units=pq.mV,
                                    sampling_period=sampling_interval)
current_analogsignal = AnalogSignal(dumper_file_data.iloc[:,1], units=pq.pA,
                                    sampling_period=sampling_interval)
figure,axes = plt.subplots(2,1,sharex='all')
axes[0].plot(voltage_analogsignal.times,np.array(voltage_analogsignal))
axes[1].plot(current_analogsignal.times,np.array(current_analogsignal))

# %%
# cell20190805A1 = SingleNeuron('20190805A1')
# all_blocks = cell20190805A1.get_blocknames(printing='off')
# recording_block = all_blocks[0]
# nonrecording_blocks = all_blocks[1:]
# for block in nonrecording_blocks:
#     cell20190805A1.rawdata_remove_nonrecordingblock(block)
# cell20190805A1.rawdata_remove_nonrecordingchannel(recording_block,2)
#
# cell20190805A1.plot_allrawdata()
# cell20190805A1.rawdata_remove_nonrecordingtimeslice(recording_block,trace_start_t=11,
#                                                     trace_end_t=38.5)
# cell20190805A1.get_depolarizingevents_fromrawdata()
# cell20190805A1.write_results()
# %%
cell20190805A2 = SingleNeuron('20190805A2')

# all_blocks = cell20190805A2.get_blocknames(printing='off')
# nonrecording_block = all_blocks[0]
# recording_blocks = all_blocks[1:]
# cell20190805A2.rawdata_remove_nonrecordingblock(nonrecording_block)
# cell20190805A2.rawdata_remove_nonrecordingchannel(recording_blocks[0],1)
#
# # cell20190805A2.plot_allrawdata(time_axis_unit='s')
# cell20190805A2.rawdata_remove_nonrecordingsection(recording_blocks[0],trace_start_t=12.7)
# cell20190805A2.rawdata_note_chemicalinbath('withBlocker')
# cell20190805A2.write_results()
plt.close('all')
a_segment = cell20190805A2.blocks[3].segments[0].time_slice(t_start=150*pq.s, t_stop=250*pq.s)
another_segment = cell20190805A2.blocks[0].segments[0].time_slice(t_start=490*pq.s, t_stop=540*pq.s)
# %%
apsdict, depolsdict = snafs.get_depolarizingevents(a_segment,
                                                   min_depolspeed=0.08,
                                                   min_depolamp=0.15,
                                                   # oscfilter_lpfreq=15,
                                                   plot='on')

anotherapsdict, anotherdepolsdict = snafs.get_depolarizingevents(another_segment,
                                                                 min_depolspeed=0.08,
                                                                 min_depolamp=0.15,
                                                                 plot='on')
# cell20190805A2.get_depolarizingevents_fromrawdata()
# cell20190805A2.plot_depolevents_overlayed(get_subthreshold_events=False,
#                                           do_baselining=True,
#                                           colorby_measure='baselinev')
# cell20190805A2.plot_depolevents_overlayed(cell20190805A2.depolarizing_events.amplitude > 3,
#                                           do_baselining=True,
#                                           colorby_measure='baselinev')