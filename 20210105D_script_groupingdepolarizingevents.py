# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210105D'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Not a great recording, with neuron barely holding -30mV resting, but has very nice responses to light
# (often fastevent, occasionally AP) and two spont.APs and a handful of spont.events.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label


# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned()



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

# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots:
# the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   plotwindow_inms=30,
                                                   prealignpoint_window_inms=15,
                                                   plot_dvdt=True
                                                   )
# fast-events:
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 and ttleffect_window=15

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=15)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# APs evoked by light got picked up OK, except in some cases baselineV point is put after the first fastevent;
# also the spont.APs get their baseline-point put after the fastevent that evokes them.
# No DC-evoked APs recorded in this neuron (DC pulses to see APs not applied).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# light-evoked responses mostly got picked up, though usually not with good baselinev-points.
# Did not see anything labeled that should in fact be spont.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# looks like spontaneous events all got picked up nicely, down to the smallest ones I could pick out by eye (pretty much exactly 2mV).

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
#
# events_underinvestigation = (unlabeled_spont_events) # & (des_df.))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# The largest two events are obviously compound; labeling them as such:
# compound_events = (unlabeled_spont_events & (des_df.amplitude > 8))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Now we are dealing with a group of events that are practically identical, except for the two largest which are much
# wider than the rest (<4ms half-width for fastevents, >5.5ms for these two). Indeed, their decay-phase looks much more
# like that of the compound events labeled previously. Labeling these as well, and the rest as fastevents:
# compound_events = (unlabeled_spont_events & (des_df.amplitude > 6))
# fastevents = (unlabeled_spont_events & (des_df.amplitude < 6))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not labeling neatevents for this neuron: resting baselineV barely -30mV throughout and barely 5 min. of recording altogether
