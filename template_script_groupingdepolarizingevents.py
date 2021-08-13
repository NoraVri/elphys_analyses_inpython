# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = ''
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
nbins = 50
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:


# des_df = singleneuron_data.depolarizing_events
# fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
# compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section
# aps = des_df.event_label == 'actionpotential'
# spont_events = ~des_df.applied_ttlpulse  # no TTL-applied experiments in this neuron
# unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
# unlabeled_spontevents = (spont_events & unlabeled_events)
# probably_spikelets = (unlabeled_spontevents & (des_df.amplitude < 1.7) & (des_df.maxdvdt < 0.12))  # see plots and analyses section

# %%
# summary plots:
# histograms of events parameters
# fast-events
# des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('fast-events parameter distributions')

# compound events
# des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('compound events parameter distributions')

# spikelets
# des_df[probably_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('probably-spikelets parameter distributions')

# action potentials
# des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('aps parameter distributions')

# line plots of the main events-groups (aps, fastevents, compound events)
# singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
#                                                    group_labels=['aps', 'compound_events', 'fastevents'],
#                                                    )

# %% plots for publication figures


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

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# 1. seeing that light/puff-evoked things all got labeled as such
evoked_events = des_df.applied_ttlpulse
singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:


# plotting events parameters:
possibly_spontfastevents_df = des_df[unlabeled_spont_events]
possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )

# plotting events:
# possibly_spontfastevents = (unlabeled_spont_events & (des_df))
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )


# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
aps = des_df.event_label == 'actionpotential'
# singleneuron_data.plot_depolevents((aps & spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
# singleneuron_data.plot_depolevents((aps & ~spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='light-evoked APs')




#### this concludes sorting through all events and labeling them ####

