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
# %% abf recordings: 3 representative example neurons - imports, cleanup and plotting of files used for testing depolarizingevents function
plt.close('all')
cell20190814A = SingleNeuron("20190814A")
file_toexcept = cell20190814A.rawdata_blocks[0].file_origin #in this block, there are 2 recording channels active but only Ch1 is actually recording from a neuron
cell20190814A.rawdata_remove_nonrecordingchannel(file_toexcept,2)
# cell20190814A.plot_block_byname(file_toexcept)
# cell20190814A.plot_block_byname(cell20190814A.rawdata_blocks[3].file_origin)

cell20190729A = SingleNeuron("20190729A")
# cell20190729A.plot_block_byname('gapFree_0001.abf')
# cell20190729A.plot_block_byname(cell20190729A.rawdata_blocks[3].file_origin)

cell20190805A = SingleNeuron('20190805A')
cell20190805A.rawdata_blocks = cell20190805A.rawdata_blocks[1::]
file_toexcept = 'gapFree_0001.abf'
cell20190805A.rawdata_remove_nonrecordingchannel(file_toexcept,1)
# cell20190805A.plot_block_byname(file_toexcept)
# cell20190805A.plot_block_byname(cell20190805A.rawdata_blocks[3].file_origin)

# %% testing the get_depolarizingevents function on each, on files with and without blockers
plt.close('all')
from singleneuron_analyses_functions import get_depolarizingevents

cell20190814Asegment_depolarizingevents = get_depolarizingevents(cell20190814A.rawdata_blocks[0].segments[0].time_slice(t_start=700*pq.s,t_stop=730*pq.s))
cell20190814Asegment_withblockers_depolarizingevents = get_depolarizingevents(cell20190814A.rawdata_blocks[3].segments[0].time_slice(t_start=230*pq.s,t_stop=260*pq.s))

# plt.figure()
# plt.plot(segment_slice.analogsignals[0].times,np.squeeze(segment_slice.analogsignals[0]))
cell20190729Asegment_depolarizingevents = get_depolarizingevents(cell20190729A.rawdata_blocks[1].segments[0].time_slice(t_start=450*pq.s,t_stop=480*pq.s))
# plt.figure()
# plt.plot(segment_withblockers_slice.analogsignals[0].times,np.squeeze(segment_withblockers_slice.analogsignals[0]))
cell20190729Asegment_withblockers_depolarizingevents = get_depolarizingevents(cell20190729A.rawdata_blocks[3].segments[0].time_slice(t_start=660*pq.s,t_stop=690*pq.s))

# plt.figure()
# plt.plot(segment_slice.analogsignals[0].times,np.squeeze(segment_slice.analogsignals[0]))
cell20190805Asegment_depolarizingevents = get_depolarizingevents(cell20190805A.rawdata_blocks[0].segments[0].time_slice(t_start=320*pq.s,t_stop=350*pq.s))
# plt.figure()
# plt.plot(segment_withblockers_slice.analogsignals[0].times,np.squeeze(segment_withblockers_slice.analogsignals[0]))
cell20190805Asegment_withblockers_depolarizingevents = get_depolarizingevents(cell20190805A.rawdata_blocks[3].segments[0].time_slice(t_start=490*pq.s,t_stop=520*pq.s))


# %%
# plt.close('all')

# # plotting raw data
# #this throws up a plot for each block that is read in
# cell20190805A.plot_allrawdata()
# # %% cleanup

