# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124C'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# quite nice recording for the most part, even though there are just 3 spont.fastevents and no spont.APs;
# baselineV quite stable for most of the recording and light seems to evoke something fast (on top of
# a slow synaptic response) practically every time.

# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()


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
# APs on currentpulses got picked up nicely; interestingly rebound AP can be evoked relatively easily,
# yet +DC does not evoke AP even when V > -20mV.
# The three light-evoked APs all got labeled appropriately; no spont.APs recorded in this neuron.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# light-evoked responses got picked up quite nicely, though baseline-points often not great;
# did not see anything labeled that should in fact be spont.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# my eyes pick up quite a lot of events with amp ~1 - 1.5mV - these all look very much like spikelets though,
# even if there were some fastevents among them I would not be able to tell them apart.
# in gapFree_0006 a single event got picked up that has to be lightevoked according to notes; labeling it as such:
# evokedevent = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0006.abf'))
# singleneuron_data.depolarizing_events.loc[evokedevent, 'applied_ttlpulse'] = True
# singleneuron_data.write_results()

# the single event that got picked up in light_0004 (amp ~18mV) is clearly compound; labeling it as such:
# compound_event = (unlabeled_spont_events & (des_df.file_origin == 'light_0004.abf'))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# now let's see what we're left with:
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

# just 5 events altogether; two have impossibly short rise-time/high maxdvdt and are probably
# noise-things from touching stuff in the rig; the others are fastevents. Labeling as such:
# singleneuron_data.depolarizing_events.loc[(unlabeled_spont_events & (des_df.rise_time_20_80 < 0.2)),
#                                           'event_label'] = 'noiseevent'
# singleneuron_data.depolarizing_events.loc[(unlabeled_spont_events & (des_df.rise_time_20_80 > 0.2)),
#                                           'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# baselineV quite stable for the first half of recording but drifting quite a bit later on; spont. fastevents
# (3 altogether in >20min. recording) don't appear until the very last block where neuron is clearly dying.
# So, I see no reason to label neat-events for this neuron.