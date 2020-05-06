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
cell20190805A.rawdata_remove_nonrecordingchannel('gapFree_0001.abf', 1)
cell20190805A.rawdata_remove_nonrecordingtimeslice('gapFree_0001.abf',
                                                   trace_start_t=13)
cell20190805A.plot_allrawdata()

# a_segment = cell20190805A.rawdata_blocks[0].segments[0].time_slice(
#     t_start=150*pq.s, t_stop=200*pq.s)

# plt.close('all')
# apsdict, depolsdict = get_depolarizingevents(a_segment,
#                                              oscfilter_lpfreq=25,
#                                              peakwindow=7,
#                                              spikeahpwindow=250, plot='on')
# %%
cell20190805A.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=25,
                                                 peakwindow=7,
                                                 spikeahpwindow=250)
cell20190805A.write_results()


cell20190814A = SingleNeuron("20190814A")
cell20190814A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# a_segment = cell20190814A.rawdata_blocks[3].segments[0].time_slice(t_start=150*pq.s,
#                                                                    t_stop=200*pq.s)
# apsdict, depolsdict = get_depolarizingevents(a_segment, plot='on')
cell20190814A.get_depolarizingevents_fromrawdata()
cell20190814A.write_results()


cell20190729A = SingleNeuron("20190729A")
# a_segment = cell20190729A.rawdata_blocks[1].segments[0].time_slice(t_start=500*pq.s,
#                                                                    t_stop=550*pq.s)

# apsdict,depolsdict = get_depolarizingevents(a_segment, spikeahpwindow=250, plot='on')

cell20190729A.get_depolarizingevents_fromrawdata(spikeahpwindow=250)
cell20190729A.write_results()


cell20200308F = SingleNeuron('20200308F')
cell20200308F.get_depolarizingevents_fromrawdata(spikeahpwindow=600)
cell20200308F.write_results()

cell20200308D = SingleNeuron('20200308D')
cell20200308D.get_depolarizingevents_fromrawdata(spikeahpwindow=200)
cell20200308D.write_results()

cell20200310C = SingleNeuron('20200310C')
cell20200310C.get_depolarizingevents_fromrawdata()
cell20200310C.write_results()
# %% plotting some stuff
cell20190805A.plot_depolevents_overlayed(get_subthreshold_events=False,
                                         colorby_measure='baselinev')

cell20190805A.plot_depolevents_overlayed((cell20190805A.depolarizing_events.amplitude > 10) &
                                         (cell20190805A.depolarizing_events['edtrace_rise_time'] < 2),
                                         do_baselining=True,
                                         colorby_measure='baselinev')

cell20190805A.plot_individualdepolevents_withmeasures((cell20190805A.depolarizing_events.amplitude > 10) &
                                         (cell20190805A.depolarizing_events['edtrace_rise_time'] < 2))
# %%
cell20190805A.plot_depolevents_overlayed((cell20190805A.depolarizing_events.amplitude > 10) &
                                         (cell20190805A.depolarizing_events.rise_time < 2),
                                         colorby_measure='applied_current')

cell20190805A.plot_depolevents_overlayed((cell20190805A.depolarizing_events.amplitude < 5) &
                                         (cell20190805A.depolarizing_events.rise_time < 2),
                                         do_baselining=True,
                                         colorby_measure='baselinev')

# cell20190805A.plot_individualdepolevents_withmeasures(
#     cell20190805A.depolarizing_events.amplitude > 20)

cell20190805A.plot_individualdepolevents_withmeasures(get_subthreshold_events=False)

# %%
cell20190814A.plot_depolevents_overlayed(get_subthreshold_events=False,
                                         colorby_measure='baselinev')

cell20190814A.plot_depolevents_overlayed(cell20190814A.depolarizing_events.amplitude > 10,
                                         do_baselining=True,
                                         colorby_measure='baselinev')

cell20190814A.plot_depolevents_overlayed((cell20190814A.depolarizing_events['edtrace_rise_time'] < 2) &
                                         (cell20190814A.depolarizing_events.amplitude > 5),
                                         do_baselining=True,
                                         colorby_measure='baselinev')

cell20190814A.plot_depolevents_overlayed((cell20190814A.depolarizing_events['edtrace_rise_time'] < 2) &
                                         (cell20190814A.depolarizing_events.amplitude > 5),
                                         do_baselining=True,
                                         do_normalizing=True,
                                         colorby_measure='baselinev')

cell20190814A.plot_individualdepolevents_withmeasures(
    (cell20190814A.depolarizing_events['edtrace_rise_time'] < 2) &
    (cell20190814A.depolarizing_events.amplitude > 5)
)

cell20190814A.plot_individualdepolevents_withmeasures(get_subthreshold_events=False)

# %%
cell20190729A.plot_depolevents_overlayed(get_subthreshold_events=False)

ivblocks_list = [filename for filename in cell20190729A.get_blocknames(printing='off') if 'IV' in filename]

cell20190729A.plot_depolevents_overlayed((cell20190729A.depolarizing_events.amplitude > 10) &
                                         (~cell20190729A.depolarizing_events.file_origin.isin(ivblocks_list)),
                                         do_baselining=True,
                                         colorby_measure='baselinev')

# %%
cell20200308F.plot_depolevents_overlayed(get_subthreshold_events=False,
                                         colorby_measure='thresholdv')

cell20200308F.plot_depolevents_overlayed(do_baselining=True,
                                         colorby_measure='baselinev')
cell20200308F.plot_depolevents_overlayed(do_baselining=True,
                                         do_normalizing=True,
                                         colorby_measure='amplitude')

# %%
cell20200308D.plot_depolevents_overlayed(get_subthreshold_events=False)

cell20200308D.plot_depolevents_overlayed(cell20200308D.depolarizing_events.amplitude > 1.2,
                                         newplot_per_block=True,
                                         do_baselining=True,
                                         colorby_measure='baselinev')

# %%
cell20200310C.plot_depolevents_overlayed(cell20200310C.depolarizing_events.amplitude > 2,
                                         colorby_measure='applied_current')

