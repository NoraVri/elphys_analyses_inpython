# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20201125D'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section2
# compound_events = des_df.event_label == 'compound_event'  # none seen
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
aps_spont = aps & spont_events
aps_evoked = aps & ~spont_events
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents & (des_df.amplitude < 4) # see plots and analyses section2

# %% summary plots - all spontaneous events:
# # histogram of baselinev in the entire recording:
# # singleneuron_data.get_timespentrecording(make_baselinev_hist=True)
# # histograms of events parameters
# nbins = 150
# # fast-events
# des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('fast-events parameter distributions')
#
#
# # spikelets
# des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('smallslowevents parameter distributions')
#
# # action potentials
# des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('aps parameter distributions')
#
# # line plots:
# # the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   )
# fast-events:
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

# scatters of events parameters:
# fast-events
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)

# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=20)
# singleneuron_data.write_results()

# %% plots and analyses: labeling depolarizing events categories
# des_df = singleneuron_data.depolarizing_events

# 1. seeing light/puff-evoked things (mostly to be sure that they're not accidentally contaminating spont.events)
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Not all evoked things got picked up as events, and baseline points are often quite bad - but none of that
# is surprising given that the evoked response is mostly 'classic' synaptic depolarization.
# Definitely nothing got picked up as evoked event that should be spontaneous.

# 2. plotting events parameters to see where to start narrowing down on fast-events:
# nbins = 100
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events
#                             )
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# from the last two plots it's very clear what should be fast-events: there are just 3 things that don't fit the bill,
# with much longer rise-time. Let's see what they are:
# notfastevents = possibly_spontfastevents & (des_df.rise_time_20_80 > 1)
# singleneuron_data.plot_rawdatablocks(*des_df[notfastevents].file_origin.unique(),
#                                      events_to_mark=notfastevents)
# the two large things are slow responses to release from hyperpolarizing current; and the third thing
# is a spikelet of ~3mV amplitude.
# labeling events:
# fastevents = (possibly_spontfastevents & ~notfastevents)
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3. Seeing that APs all got picked up properly
# spont_aps = (aps & spont_events)
# evoked_aps = (aps & evoked_events)
# singleneuron_data.plot_rawdatablocks(*des_df[spont_aps].file_origin.unique(),
#                                      events_to_mark=spont_aps)
# singleneuron_data.plot_rawdatablocks(*des_df[evoked_aps].file_origin.unique(),
#                                      events_to_mark=evoked_aps)
# all looks great.


# %% plots for publication figures -- MSdraft version3 (APs first), figure 1
# this neuron has just 13 fastevents and 16 APs (a bunch of which are evoked) altogether, so gonna use all of them
# selecting a short trace to serve as example of spont. activity
# singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=fastevents)

aps_axis, aps_dvdt_axis = singleneuron_data.plot_depolevents((aps & spont_events
                                    ),
                                   colorby_measure='baselinev',
                                   timealignto_measure='rt20_start_idx',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=2,
                                   plotwindow_inms=18,
                                   )

fastevents_axis, fastevents_dvdt_axis = singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   timealignto_measure='rt20_start_idx',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=2,
                                   plotwindow_inms=18,
                                   )
#
# # saving the figures, then re-scaling axes:
aps_axis.set_xlim([0, 3])
aps_axis.set_ylim([-1, 15])
aps_dvdt_axis.set_ylim([-0.15, 1.15])
aps_dvdt_axis.set_xlim([-1, 15])

fastevents_axis.set_xlim([0, 3])
fastevents_axis.set_ylim([-1, 15])
fastevents_dvdt_axis.set_ylim([-0.15, 1.15])
fastevents_dvdt_axis.set_xlim([-1, 15])





# %% plotting light-evoked activity
# light intensity is identical for all traces, except light_0003 trace1 where light wasn't on
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True,)
# there are different TTL durations, however, only with the longest one does the recording also cover the
# full dynamic range of the neuron.

figure, axes = singleneuron_data.plot_rawdatatraces_ttlaligned('light_0002',
                                                skip_vtraces_idcs=[9, 10, 11, 12, 13,])
# save figure, then re-scaling axes:
axes[0].set_xlim([-0.5, 11.5])
axes[0].set_ylim([-1, 15])
axes[1].set_ylim([-0.15, 1.15])
axes[1].set_xlim([-1, 15])

# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=20)
# singleneuron_data.write_results()
# %% seeing spont.APs
des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #

singleneuron_data.plot_depolevents((aps & spont_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' spont aps'
                                   )

