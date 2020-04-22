# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 11:21:16 2020

@author: neert

In this script: 'representative' neuron recordings (abf and pxp);
get_depolarizingevents function tested on (a time slice of) a segment from each (with and without blockers, in the case of the abf recordings).
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import quantities as pq

os.chdir("D:\\hujigoogledrive\\research_YaromLabWork\\Code_inPython\\elphysDataAnalyses_working")
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_depolarizingevents

# %% importing of a couple of 'best representative' recordings
cell20190805A = SingleNeuron('20190805A')
cell20190805A.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
cell20190805A.rawdata_remove_nonrecordingchannel('gapFree_0001.abf',1)
# %%
cell20190814A = SingleNeuron("20190814A")
cell20190814A.rawdata_remove_nonrecordingchannel(cell20190814A.rawdata_blocks[0].file_origin,2)

cell20190729A = SingleNeuron("20190729A")

cell20200308B = SingleNeuron('20200308B')

cell20200308F = SingleNeuron('20200308F')

cell20200308D = SingleNeuron('20200308D')

cell20200310C = SingleNeuron('20200310C')



# %% small sections, while plotting everything
(cell20190814Asegment_actionpotentials,
 cell20190814A_depolarizingevents) = get_depolarizingevents(
    cell20190814A.rawdata_blocks[0].segments[0].time_slice(t_start=710*pq.s,t_stop=711*pq.s))
# %%
(cell20190814Asegment_withblockers_actionpotentials,
 cell20190814Asegment_withblockers_depolarizingevents) = get_depolarizingevents(
    cell20190814A.rawdata_blocks[3].segments[0].time_slice(t_start=230*pq.s,t_stop=260*pq.s))

# %%
(cell20190805Asegment_actionpotentials,
 cell20190805Asegment_depolarizingevents) = get_depolarizingevents(
    cell20190805A.rawdata_blocks[0].segments[0].time_slice(t_start=325*pq.s,t_stop=336*pq.s))
# %%
(cell20190805Asegment_withblockers_actionpotentials,
 cell20190805Asegment_withblockers_depolarizingevents) = get_depolarizingevents(
    cell20190805A.rawdata_blocks[3].segments[0].time_slice(t_start=50*pq.s,t_stop=350*pq.s))

# %%
(cell20190729Asegment_actionpotentials,
 cell20190729Asegment_depolarizingevents) = get_depolarizingevents(
    cell20190729A.rawdata_blocks[1].segments[0].time_slice(t_start=450*pq.s,t_stop=480*pq.s))
# %%
(cell20190729Asegment_withblockers_actionpotentials,
 cell20190729Asegment_withblockers_depolarizingevents) = get_depolarizingevents(
    cell20190729A.rawdata_blocks[3].segments[0].time_slice(t_start=660*pq.s,t_stop=690*pq.s))

# %% pxp recording
(cell20200308Bsegment_actionpotentials,
 cell20200308Bsegment_depolarizingevents) = get_depolarizingevents(
    cell20200308B.rawdata_blocks[8].segments[0].time_slice(t_start=140*pq.s,t_stop=170*pq.s))
(cell20200308Bsegment_withlightpulse_actionpotentials,
 cell20200308Bsegment_withlightpulse_depolarizingevents) = get_depolarizingevents(
    cell20200308B.rawdata_blocks[0].segments[0])
