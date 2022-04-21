# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = ''
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:


des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise

# %% summary plots - all events:
# histogram of baselinev in the entire recording:
# singleneuron_data.get_timespentrecording(make_baselinev_hist=True)
# histograms of events parameters
nbins = 100
# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('fast-events parameter distributions')

# compound events
des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('compound events parameter distributions')

# spikelets
des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('smallslowevents parameter distributions')

# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots:
# the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
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
# %% summary plots - neat events only:
nbins = 100  #
neat_events = singleneuron_data.depolarizing_events.neat_event
# fast-events
singleneuron_data.plot_depolevents((fastevents & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events'
                                   )
des_df[(fastevents & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                        'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                        bins=nbins)
plt.suptitle('fast-events, neat ones only')

# compound events
singleneuron_data.plot_depolevents((compound_events & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat compound events'
                                   )
des_df[(compound_events & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                             bins=nbins)
plt.suptitle('compound events, neat ones only')

# aps
singleneuron_data.plot_depolevents((aps & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat aps'
                                   )
des_df[(aps & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                             bins=nbins)
plt.suptitle('aps, neat ones only')

# %% plots: fast-events normalized and averaged
# setup - marking amplitude- and baselinev-groups
# baselinevgroup1 = (des_df.baselinev < )
# baselinevgroup2 = (des_df.baselinev > )
# ampgroup1 = (fastevents & neat_events & (des_df.amplitude < ))
#
# # fast-events normalized, averaged per baselinev group
# singleneuron_data.plot_depoleventsgroups_averages((fastevents & neat_events & baselinevgroup1),
#                                                   (fastevents & neat_events & baselinevgroup2),
#                                                   group_labels=['low baselinev', 'high baselinev'],
#                                                   plotwindow_inms=20,
#                                                   do_normalizing=True,
#                                                   )
#
# # fast-events averaged per amplitude group (sorted by eye), separately for 2 baselinev values
# singleneuron_data.plot_depoleventsgroups_averages((ampgroup1 & baselinevgroup1),
#                                                   (ampgroup2 & baselinevgroup1),
#                                                   (ampgroup3 & baselinevgroup1),
#                                                   (ampgroup4 & baselinevgroup1),
#                                                   (ampgroup5 & baselinevgroup1),
#                                                   group_labels=['group1', 'group2', 'group3', 'group4', 'group5'],
#                                                   plotwindow_inms=20,
#                                                   plt_title='baselinev < mV'
#                                                   )
# singleneuron_data.plot_depoleventsgroups_averages((ampgroup1 & baselinevgroup2),
#                                                   (ampgroup2 & baselinevgroup2),
#                                                   (ampgroup3 & baselinevgroup2),
#                                                   (ampgroup4 & baselinevgroup2),
#                                                   (ampgroup5 & baselinevgroup2),
#                                                   group_labels=['group1', 'group2', 'group3', 'group4', 'group5'],
#                                                   plotwindow_inms=20,
#                                                   plt_title='baselinev > mV'
#                                                   )


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:


# block_no = 0
# segment_no = 0
# time_slice = [100, 250]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
# check that AHP width window wide enough
# )

# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# singleneuron_data.plot_rawdatablocks(*blocknames,
#                                      events_to_mark=events,
#                                      segments_overlayed=False)

# %% plots and analyses: seeing and labeling subthreshold depolarizing events categories
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:


# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting all as-yet unlabeled events parameters:
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# Labeling fast-events and other events fitting in categories not labeled automatically (fastevent, compound_event, other_event, noiseevent)
# 1.

# events_underinvestigation = (unlabeled_spont_events & (des_df.))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )





#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# neurons that were recorded under bad conditions for the entire duration of recording should not get neat_events marked.
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)
# notes:

# ... min. of recording from file , from s to s
# block_name = ''
# window_start_t =
# window_end_t =
# sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
# if block_name in singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'].keys():
#     trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'][block_name]['t_start']
# else: trace_start_t = 0
# neat5min_start_idx = (window_start_t - trace_start_t) * float(sampling_frequency)
# neat5min_end_idx = (window_end_t - trace_start_t) * float(sampling_frequency)
# probably_neatevents = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx >= neat5min_start_idx)
#                        & (des_df.peakv_idx < neat5min_end_idx)
#                        )
# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()
# %% marking 'n neat fast events': the first 10 - 20 events to occur during stable recording at resting baselinev
# neurons with < 10 neat spont. fast-events should not get them marked; those with > 20 get the first 20 that occur marked, regardless of representativeness of amplitude groups etc.
fastevents = ((des_df.event_label == 'fastevent') & (des_df.neat_event))
neatevents = fastevents.copy()
neatevents[neatevents] = False
fastevents = fastevents[fastevents]
n = 19  # N - 1 (0-based indexing)
i = 0
# check that these events occur during resting baselinev
for idx, value in fastevents.iteritems():
    if i <= 19:
        neatevents[idx] = True
        i += 1
    else:
        break
neatevents.name = 'n_neat_fastevents'
# adding the neatevents-series to the depolarizing_events-df:
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neatevents)
# singleneuron_data.write_results()
# %% plots and analyses: seeing APs and labeling fast-event triggered ones

