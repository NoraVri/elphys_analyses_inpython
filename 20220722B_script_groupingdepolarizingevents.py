# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220722B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# Neuron starts off doing lots of fastevents and APs spontaneously, then APs cease to occur after ~10min. but
# fastevents (amp up to 7mV or so) continue. Also has TONS of events with amp up to ~3mV.
# Under TTX application event frequencies decrease slowly, and occasional events with amps ~3mV continue to occur
# (and become more frequent again with washout, though neuron itself does not regain the ability to make Na-APs).

# %% summary plots
des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #

# histograms of events parameters
nbins = 100
# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('fast-events parameter distributions')
# aps
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots
# fast-events:
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# aps:
singleneuron_data.plot_depolevents(aps,
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
# extracting with default parameter settings except min_depolamp=2 to make sure we can separate between large spikelets and small fastevents

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: one got labeled as such in gapFree_0000 but it actually comes just before a (small) currentpulsechange; re-labeling it as spont.:
# spontap = (aps_oncurrentpulsechange & (des_df.file_origin == 'gapFree_0000.abf'))
# singleneuron_data.depolarizing_events.loc[spontap, 'event_label'] = 'actionpotential'
# and in gapFree_withTTXwashout_0000 things got labeled as APs even though they're just a mostly passive response to
# large depolarizing current. Labeling them as currentpulsechange:
# currentpulsechanges = (aps_oncurrentpulsechange & (des_df.file_origin == 'gapFree_withTTXwashout_0000.abf'))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# aps_spont: looks like they all got picked up quite nicely automatically.

singleneuron_data.plot_depolevents(aps_spont,
                                   colorby_measure='baselinev')


# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# blocknames = des_df[unlabeled_spont_events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=unlabeled_spont_events,
#                                          segments_overlayed=False)
# notes:
# the cutoff amplitude of 2mV still seems rather arbitrary given the data; there are lots of events with amp 1-3mV.
# Nonetheless, I'm quite confident that if any of them are proper fastevents, they did get picked up.
# Didn't see anything labeled that shouldn't've been.

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting all as-yet unlabeled events parameters:
des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
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
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
# well, this is gonna be interesting - my gut says a LOT of these events should be spikelets, but by parameter
# distributions I don't see much of a clear cutoff into two big groups of events (though there are some outliers on every parameter).

# Let's sort through all these in groups by baselineV.
# Group1: baselineV < -52mV
# In this group, there are two events with much longer rise-time than all the others (1.2-1.4ms vs ~0.4-0.8 ms for
# the rest). One of these has very large amp (14 mV) and is clearly a compound event; the other one is very small (~2mV)
# and not a fastevent, in my opinion. Labeling events accordingly:
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev < -52))
# compound_event = (events_underinvestigation & (des_df.amplitude > 12))
# fastevents = (events_underinvestigation & (des_df.rise_time_20_80 < 1))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Group2: baselineV < -44
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev < -44) & (des_df.baselinev >= -52))
# This group is all fastevents: there are some that have slower maxdvdt than most, but the waveforms are exactly
# identical and the elapsed recording time in between can account for that. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Group3: baselineV > -35.5
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev > -35.5))
# there are three events of amp ~2mV there, while the rest is >4mV; nonetheless, I am convinced they are all fastevents
# (waveform shapes are identical, parameter distributions show no groupings or even outliers, and the smallest events
# do not have the slowest rise-time of the bunch). Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Group4: baselineV > -38
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev > -38))
# except for one 'event' that has way too small rise-time to be anything but noise, once again it seems these should
# all be classified as fastevents.
# noiseevent = (events_underinvestigation & (des_df.rise_time_20_80 < 0.2))
# fastevents = (events_underinvestigation & ~noiseevent)
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Group5: baselineV > -40
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev > -40))
# I once again cannot find any objection to labeling all these events as fastevents, even though amps are as small as 2mV.
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Group6: baselineV > -41
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev > -41))
# in rise-time it seems there are some outliers; indeed, looking at events with rise-time >0.9ms these are double-events (and one of 3mV that might not be).
# Labeling them as compound events, and the rest as fastevents:
# compound_events = (events_underinvestigation & (des_df.rise_time_20_80 > 0.9))
# fastevents = (events_underinvestigation & ~compound_events)
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# Group7: rise-time_20_80 > 0.9ms
# In the now remaining events, it starts to look like outliers might be characterized by long rise-time and low max.dVdt.
# Indeed, seeing the 6 events with rise-time > 0.9ms shows three with large amplitude (6-7mV) that look like compound
# events, and three with small amplitude (<3mV) that have dVdt up to ~0.1mV/ms. Seeing them in the raw data they are
# all from the first recording file, which strengthens me in my belief that these are spikelets, not fastevents.
# Labeling events accordingly:
# events_underinvestigation = (unlabeled_spont_events & (des_df.rise_time_20_80 > 0.9))
# compound_events = (events_underinvestigation & (des_df.amplitude > 6))
# fastevents = (unlabeled_spont_events & (des_df.rise_time_20_80 <= 0.9))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
#
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# events = (events_underinvestigation & (des_df.amplitude < 3))
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

# singleneuron_data.get_depolarizingevents_frequencies_byrecordingblocks()
sorted = singleneuron_data.recordingblocks_index.sort_values('file_timestamp')
