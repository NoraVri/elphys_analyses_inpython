# in this script: an initial batch of neurons representing all the different types of experiments
# (RubiGlu-uncaging; blocking synaptic inputs; exciting the (synaptic inputs to) the neurons).

# %% imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quantities as pq

from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_depolarizingevents

# %% activating synaptic inputs optogenetically example
cell20190529D = SingleNeuron('20190529D')
cell20190529D.rawdata_remove_nonrecordingsection('gapFree_0001.abf',
                                                 trace_end_t=395)
# cell20190529D.plot_blocks_byname('gapFree_0001.abf', time_axis_unit='s')
# cell20190529D.plot_allrawdata()
# cell20190529D.write_results()
# %%
# for i, _ in enumerate(cell20190529D.blocks[2].segments):
#     apsdict, depolsdict = cell20190529D.plot_eventdetecttraces_forsegment(2,i,return_dicts=True,
#                                                                       oscfilter_lpfreq=5,
#                                                                       noisefilter_hpfreq=2000,
#                                                                       min_depolspeed=0.15,
#                                                                       peakwindow=10)
cell20190529D.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=5,
                                                 noisefilter_hpfreq=2000,
                                                 min_depolspeed=0.15,
                                                 peakwindow=10,
                                                 ttleffect_windowinms=10)
cell20190529D.write_results()

# plotting stuff
figure, axes = plt.subplots(2, 2)
cell20190529D.depolarizing_events.plot.scatter(x='amplitude',
                                               y='rise_time',
                                               c='baselinev',
                                               colormap='viridis',
                                               ax=axes[0,0])
cell20190529D.depolarizing_events.plot.scatter(x='edtrace_amplitude',
                                               y='edtrace_rise_time',
                                               c='baselinev',
                                               colormap='viridis',
                                               ax=axes[1,0])
cell20190529D.depolarizing_events.plot.scatter(x='half_width',
                                               y='rise_time',
                                               c='amplitude',
                                               colormap='viridis',
                                               ax=axes[0,1])
cell20190529D.depolarizing_events.plot.scatter(x='edtrace_half_width',
                                               y='edtrace_rise_time',
                                               c='amplitude',
                                               colormap='viridis',
                                               ax=axes[1,1])

# %%
# let's see light-evoked and spontaneous events separately
evokedevents = cell20190529D.depolarizing_events[cell20190529D.depolarizing_events.applied_ttlpulse]
spontevents = cell20190529D.depolarizing_events[(~cell20190529D.depolarizing_events.applied_ttlpulse)]

figure2, axes = plt.subplots(2,2)
evokedevents.plot.scatter(x='amplitude',
                          y='rise_time',
                          c='baselinev',
                          colormap='viridis',
                          ax=axes[0,0])
spontevents.plot.scatter(x='amplitude',
                          y='rise_time',
                          c='baselinev',
                          colormap='viridis',
                          ax=axes[1,0])

evokedevents.plot.scatter(x='half_width',
                          y='rise_time',
                          c='amplitude',
                          colormap='viridis',
                          ax=axes[0,1])
spontevents.plot.scatter(x='half_width',
                          y='rise_time',
                          c='amplitude',
                          colormap='viridis',
                          ax=axes[1,1])
plt.suptitle('evoked events (top row) and spontaneous events (bottom row)')

probablyfastevents_evoked = ((cell20190529D.depolarizing_events.amplitude > 2.5)
                             & (cell20190529D.depolarizing_events.rise_time < 3.5)
                             & cell20190529D.depolarizing_events.applied_ttlpulse)

probablyfastevents_spont = ((cell20190529D.depolarizing_events.amplitude > 2.5)
                             & (cell20190529D.depolarizing_events.rise_time < 3.5)
                             & ~cell20190529D.depolarizing_events.applied_ttlpulse)

cell20190529D.plot_depolevents_overlayed(probablyfastevents_evoked,
                                         do_baselining=True,
                                         colorby_measure='baselinev',
                                         plt_title='probably all fast events, evoked')
cell20190529D.plot_depolevents_overlayed(probablyfastevents_spont,
                                         do_baselining=True,
                                         colorby_measure='baselinev',
                                         plt_title='probably all fast events, spontaneously occurring')



# %% plotting the action potentials
cell20190529D.plot_depolevents_overlayed(cell20190529D.action_potentials.applied_ttlpulse,
                                         get_subthreshold_events=False,
                                         do_baselining=True,
                                         colorby_measure='baselinev')
plt.suptitle('evoked spikes')
cell20190529D.plot_depolevents_overlayed(~cell20190529D.action_potentials.applied_ttlpulse,
                                         get_subthreshold_events=False,
                                         do_baselining=True,
                                         colorby_measure='baselinev')
plt.suptitle('spontaneous spikes')

# %% synaptic inputs blocking example
# # %% importing the raw data for the first time and cleaning it
# cell20190812A = SingleNeuron('20190812A')
# # cell20190812A.rawdata_remove_nonrecordingchannel('gapFree_0000.abf', 2)
# # cell20190812A.rawdata_remove_nonrecordingsection('gapFree_0000.abf', 98)
# # cell20190812A.rawdata_remove_nonrecordingsection('gapFree_withBlockers_0003.abf', 300)  # time it takes for blockers to reach bath
# # cell20190812A.rawdata_note_chemicalinbath('withBlockers')
# # cell20190812A.plot_blocks_byname('gapFree_0000.abf', time_axis_unit='s')
# # cell20190812A.write_results()
# # cell20190812A.plot_allrawdata()
#
# # # %% finding good (enough) parameter settings for finding depolarizing events, and then getting them
# allblocks_names = cell20190812A.get_blocknames(printing='off')
# spontactivity_blocksnames = [block for block in allblocks_names if 'gapFree' in block]
# # cell20190812A.plot_blocks_byname(*spontactivity_blocksnames, time_axis_unit='s')
# # testblocks_idcs = [1, 3]
# # for block_idx in testblocks_idcs:
# #     a_segment = cell20190812A.blocks[block_idx].segments[0].time_slice(t_start=500*pq.s,
# #                                                                        t_stop=650*pq.s)
# #     apsdict, depolsdict = get_depolarizingevents(a_segment,
# #                                                  oscfilter_lpfreq=15,
# #                                                  min_depolspeed=0.13,
# #                                                  min_depolamp=0.15,
# #                                                  spikeahpwindow=225,
# #                                                  plot='on')
# # phase estimation not really working where oscillations are small (< 5 mV)
# # this neuron has fast-events as small as 0.5 mV for sure
# # cell20190812A.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=15,
# #                                                  min_depolspeed=0.13,
# #                                                  min_depolamp=0.15,
# #                                                  spikeahpwindow=250)
# # cell20190812A.write_results()
# # cell20190812A.plot_eventdetecttraces_forsegment(1, 0)
# # cell20190812A.plot_eventdetecttraces_forsegment(3, 0)
#
# # %% taking a look at all the events by their measurements
# cell20190812A.depolarizing_events.plot.scatter(x='edtrace_rise_time',
#                                                y='edtrace_amplitude',
#                                                c='edtrace_half_width',
#                                                colormap='viridis')
# plt.suptitle('all detected events')
#
# cell20190812A.depolarizing_events.plot.scatter(x='rise_time',
#                                                y='amplitude',
#                                                c='baselinev',
#                                                colormap='viridis')
# plt.suptitle('all detected events')
#
# cell20190812A.depolarizing_events.plot.scatter(x='rise_time',
#                                                y='amplitude',
#                                                c='half_width',
#                                                colormap='viridis')
# plt.suptitle('all detected events')
# # clearly there are fast-events: rise-time < 1 ms and amp up to 15 mV but unclear how small it can be.
# # %% plotting only events from traces with/without blockers applied
# chemicalsapplied_blocks = cell20190812A.rawdata_readingnotes['chemicalsapplied_blocks']
# chemicalsapplied_events = False
# for block in chemicalsapplied_blocks:
#     block_events = (cell20190812A.depolarizing_events.file_origin == block)
#     chemicalsapplied_events = (chemicalsapplied_events | block_events)
# chemicalsapplied_events_df = cell20190812A.depolarizing_events[chemicalsapplied_events]
#
# chemicalsapplied_events_df.plot.scatter(x='rise_time',
#                                         y='amplitude',
#                                         c='baselinev',
#                                         colormap='viridis')
# # with synaptic inputs blocked, events that still occur are <1 mV.
# cell20190812A.plot_depolevents_overlayed(cell20190812A.depolarizing_events.amplitude > 0.1,
#                                          blocknames_list=chemicalsapplied_blocks,
#                                          # newplot_per_block=True,
#                                          plt_title='synaptic blockers applied',
#                                          do_baselining=True,
#                                          colorby_measure='baselinev')
#
# nochemicalsapplied_blocks = [block for block in allblocks_names if block not in chemicalsapplied_blocks]
# nochemicalsapplied_events = False
# for block in nochemicalsapplied_blocks:
#     block_events = (cell20190812A.depolarizing_events.file_origin == block)
#     nochemicalsapplied_events = (nochemicalsapplied_events | block_events)
# nochemicalsapplied_events_df = cell20190812A.depolarizing_events[nochemicalsapplied_events]
#
# nochemicalsapplied_events_df.plot.scatter(x='rise_time',
#                                         y='amplitude',
#                                         c='baselinev',
#                                         colormap='viridis')
# # it's strange because without blockers, there are plenty of slow-risetime events of 1 - 2mV.
# intermediateamp_events = ((cell20190812A.depolarizing_events.amplitude > 1)
#                           & (cell20190812A.depolarizing_events.amplitude < 5)
#                           & (cell20190812A.depolarizing_events.baselinev < -20))
# cell20190812A.plot_depolevents_overlayed(intermediateamp_events,
#                                          blocknames_list=nochemicalsapplied_blocks,
#                                          timealignto_measure='baselinev_idx',
#                                          prealignpoint_window_inms=20,
#                                          total_plotwindow_inms=100,
#                                          do_baselining=True,
#                                          colorby_measure='baselinev',
#                                          plt_title='intermediate-amplitude events')
#
# cell20190812A.depolarizing_events[intermediateamp_events].plot.scatter(x='rise_time',
#                                                                        y='half_width',
#                                                                        c='amplitude',
#                                                                        colormap='viridis')
# cell20190812A.depolarizing_events[intermediateamp_events].plot.scatter(x='rise_time',
#                                                                        y='amplitude',
#                                                                        c='half_width',
#                                                                        colormap='viridis')
# # %%
# probablyfastevents = ((cell20190812A.depolarizing_events.rise_time < cell20190812A.depolarizing_events.amplitude)
#                       & (cell20190812A.depolarizing_events.amplitude > 0.1)
#                       & (cell20190812A.depolarizing_events.baselinev < -20))
# cell20190812A.plot_depolevents_overlayed(probablyfastevents,
#                                          do_baselining=True,
#                                          colorby_measure='baselinev',
#                                          prealignpoint_window_inms=20,
#                                          total_plotwindow_inms=70,
#                                          plt_title='probably all fast-events')
# # there seems to be two groups: those with amp > 5.5mV, and those < 3.5 mV.
# largefastevents = (probablyfastevents
#                    & (cell20190812A.depolarizing_events.amplitude > 5))
# cell20190812A.plot_depolevents_overlayed(largefastevents,
#                                          do_baselining=True,
#                                          colorby_measure='baselinev',
#                                          prealignpoint_window_inms=100,
#                                          total_plotwindow_inms=300,
#                                          plt_title='large-amplitude fast-events')
# cell20190812A.plot_depolevents_overlayed(largefastevents,
#                                          do_baselining=True,
#                                          do_normalizing=True,
#                                          colorby_measure='baselinev',
#                                          prealignpoint_window_inms=100,
#                                          total_plotwindow_inms=300,
#                                          plt_title='large-amplitude fast-events')
#
# smallevents = (probablyfastevents
#                & (cell20190812A.depolarizing_events.amplitude < 5))
# cell20190812A.plot_depolevents_overlayed(smallevents,
#                                          do_baselining=True,
#                                          do_normalizing=True,
#                                          colorby_measure='baselinev',
#                                          prealignpoint_window_inms=100,
#                                          total_plotwindow_inms=300,
#                                          plt_title='small-amplitude fast-events')
#
# bins_sequence = np.arange(0, int(cell20190812A.depolarizing_events.amplitude.max() + 1), 0.25)
# cell20190812A.depolarizing_events[probablyfastevents].hist('amplitude',
#                                                         bins=bins_sequence)
# plt.suptitle('probably all fast-events')


# %% RubiGlu-uncaging example
# # %% importing the raw data for the first time and cleaning it
# plt.close('all')
# cell20200310G = SingleNeuron('20200310G')
# # cell20200310G.plot_allrawdata()
# # cell20200310G.rawdata_remove_nonrecordingsection('R21_lighttriggered_CCmode.ibw',
# #                                                  segment_idx=1)
# # cell20200310G.plot_blocks_byname('R21_lighttriggered_CCmode.ibw', segments_overlayed=False)
# # cell20200310G.write_results()
# # %% finding good (enough) parameter settings for finding depolarizing events, and then getting them
# # allblocks_names = cell20200310G.get_blocknames(printing='off')
# # spontactivity_blocksnames = [blockname for blockname in allblocks_names
# #                              if 'spontactivity' in blockname]
# # for block in spontactivity_blocksnames:
# #     block_idx = allblocks_names.index(block)
# #     a_segment = cell20200310G.blocks[block_idx].segments[0].time_slice(t_start=30*pq.s,
# #                                                                        t_stop=50*pq.s)
# #     apsdict, depolsdict = get_depolarizingevents(a_segment,
# #                                                  oscfilter_lpfreq=30,
# #                                                  min_depolamp=0.15,
# #                                                  spikeahpwindow=125,
# #                                                  plot='on')
#
# # cell20200310G.get_depolarizingevents_fromrawdata(oscfilter_lpfreq=30)
# # cell20200310G.write_results()
# # %% checking that extracted depolarizing events look OK
# all_blocks = cell20200310G.get_blocknames(printing='off')
# # cell20200310G.plot_blocks_byname(*all_blocks,
# #                                  events_to_mark=cell20200310G.depolarizing_events)
#
# # blocks_withspikes = list(set(cell20200310G.action_potentials.file_origin))
# # cell20200310G.plot_blocks_byname(*blocks_withspikes,
# #                                  events_to_mark=cell20200310G.action_potentials)
# spontactivity_blocks = [block for block in all_blocks if 'spont' in block]
# # cell20200310G.plot_blocks_byname(*spontactivity_blocks,
# #                                  events_to_mark=cell20200310G.depolarizing_events)
#
# # %% taking a look at all the events by their measurements
# cell20200310G.depolarizing_events.plot.scatter(x='rise_time',
#                                                y='amplitude',
#                                                c='half_width',
#                                                colormap='viridis')
# plt.suptitle('all detected events')
#
# cell20200310G.depolarizing_events.plot.scatter(x='edtrace_rise_time',
#                                                y='edtrace_amplitude',
#                                                c='edtrace_half_width',
#                                                colormap='viridis')
# plt.suptitle('all detected events')
#
# cell20200310G.depolarizing_events.plot.scatter(x='rise_time',
#                                                y='amplitude',
#                                                c='baselinev',
#                                                colormap='viridis')
# plt.suptitle('all detected events')
#
# # %% getting only events from the cleanest (parts of), longest traces for (initial) analyses
# # plt.close('all')
# # i = 3
# # cell20200310G.plot_eventdetecttraces_forsegment(all_blocks.index(spontactivity_blocks[i]),0)
#
# # %%
# sliceendtime = 295 # seconds; after this time the phase as gotten from the hilbert-transform looks messed-up
# sliceendidx = (float(cell20200310G.blocks[
#                         all_blocks.index(spontactivity_blocks[0])].segments[0].analogsignals[0].sampling_rate)
#                * sliceendtime)
# cleansegment1_events = ((cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[0])
#                     & (cell20200310G.depolarizing_events.baselinev_idx < sliceendidx))
# cleansegment2_events = (cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[1])
# # ! In this following segment, 'leftovers' of oscillations/dendritic spiking are consistently
# # picked up as events of ~1 - 1.5 mV. It is also the one spontactivity recording before bath-application of RubiGlu.
# cleansegment3_events = (cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[2])
# # ! In this following segment, RubiGlu reaches the bath after ~10 min. (no qualitative change in behavior, in my eyes.)
# cleansegment4_events = (cell20200310G.depolarizing_events.file_origin == spontactivity_blocks[3])
#
# cleansegments_events = (cleansegment1_events | cleansegment2_events | cleansegment3_events | cleansegment4_events)
#
# # %% taking a look at event-measures distributions
# cell20200310G.depolarizing_events[cleansegments_events].plot.scatter(x='rise_time',
#                                                                      y='amplitude',
#                                                                      c='half_width',
#                                                                      colormap='viridis')
# plt.suptitle('events detected in spont.activity traces')
# cell20200310G.depolarizing_events[cleansegments_events].plot.scatter(x='rise_time',
#                                                                      y='amplitude',
#                                                                      c='baselinev',
#                                                                      colormap='viridis')
# plt.suptitle('events detected in spont.activity traces')
# cell20200310G.depolarizing_events[cleansegments_events].plot.scatter(x='edtrace_rise_time',
#                                                                      y='edtrace_amplitude',
#                                                                      c='edtrace_half_width',
#                                                                      colormap='viridis')
# plt.suptitle('events detected in spont.activity traces')
#
# # %% from the ed-trace scatter there is clearly a group of fast-events: rise-time < 1ms, amp > 1mV (both raw and ed)
# fastevents = ((cell20200310G.depolarizing_events.edtrace_rise_time < 1)
#               & (cell20200310G.depolarizing_events.edtrace_amplitude > 1)
#               & (cell20200310G.depolarizing_events.baselinev < -30))
#
# # plotting the events themselves, baselined, colored by baselinev
# cell20200310G.plot_depolevents_overlayed((cleansegments_events & fastevents),
#                                          do_baselining=True,
#                                          colorby_measure='baselinev')
# cell20200310G.plot_depolevents_overlayed((cleansegments_events & fastevents),
#                                          do_baselining=True,
#                                          colorby_measure='baselinev',
#                                          get_measures_type='edtrace')
#
# # seeing the histogram of event amplitudes:
# # (there should be clear peaks for distinct groups)
# bins_sequence = np.arange(0, int(cell20200310G.depolarizing_events.amplitude.max() + 1), 0.25)
#
# cell20200310G.depolarizing_events[cleansegments_events & fastevents].hist('amplitude',
#                                                                           bins=bins_sequence)
# plt.suptitle('fast events from clean data')
#
# # seeing the normalized waveform:
# # (the waveforms should be identical, though lower baselinev should lead to slower decay)
# cell20200310G.plot_depolevents_overlayed((cleansegments_events & fastevents),
#                                          do_baselining=True,
#                                          do_normalizing=True,
#                                          colorby_measure='baselinev')
#
# # seeing the relationship between rise-time and half-width:
# # (there should be no relationship, though lower baselinev should lead to increased half-width)
# cell20200310G.depolarizing_events[cleansegments_events
#                                   & fastevents].plot.scatter(x='rise_time',
#                                                              y='half_width',
#                                                              c='baselinev',
#                                                              colormap='viridis')
#
#
# # %% generalizing to all data
# # plotting the events themselves, baselined, colored by baselinev
# cell20200310G.plot_depolevents_overlayed((fastevents),
#                                          do_baselining=True,
#                                          colorby_measure='baselinev')
# cell20200310G.plot_depolevents_overlayed((fastevents),
#                                          do_baselining=True,
#                                          colorby_measure='baselinev',
#                                          get_measures_type='edtrace')
#
# # seeing the histogram of event amplitudes:
# # (there should be clear peaks for distinct groups)
# cell20200310G.depolarizing_events[fastevents].hist('amplitude',
#                                                    bins=bins_sequence)
#
# # seeing the normalized waveform:
# # (the waveforms should be identical, though lower baselinev should lead to slower decay)
# cell20200310G.plot_depolevents_overlayed((fastevents),
#                                          do_baselining=True,
#                                          do_normalizing=True,
#                                          colorby_measure='baselinev')
#
# # seeing the relationship between rise-time and half-width:
# # (there should be no relationship, though lower baselinev should lead to increased half-width)
# cell20200310G.depolarizing_events[fastevents].plot.scatter(x='rise_time',
#                                                            y='half_width',
#                                                            c='baselinev',
#                                                            colormap='viridis',
#                                                            title='fast events from all data')
#
#
# # %% don't forget about looking at things relative to oscs eventually
# # cell20200310G.depolarizing_events[cleansegments_events & fastevents].hist('approx_oscinstphase',
# #                                                                           bins=20,
# #                                                                           range=[-3.2, 3.2])
#


