# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190401A1'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
#


# summary plots:


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# pretty nice recording overall, though the first few minutes (gapFree 1 and 2) the recording conditions seem to be
# changing a bit periodically.
# Neuron is initially not oscillating, but finds its rhythm and sticks to it (pretty wacky for the most part).
# Has LOADS of fast-events and spont.APs initially, but frequency decreasing; first spont.APs go, by the end I
# don't see any fast-events anymore either (shortPulse and gapFree 3).

# I will use the end of gapFree_0002 (where neuron has started doing its steady oscillations) and
# gapFree_0003 (where there's no obviously visible fast-events, but I do still see spikelets on the oscillations).

# for the most part the standard parameter settings work great. I increased min_depolspeed and min_depolamp to really
# narrow down on events only; in neat stretches of recording the event-detect-trace derivative noise being is mostly
# <0.1mV/ms and real events stand out really nicely (reaching 0.15 easily), but in noisier stretches of recording we'll be
# catching a lot of noise-events with that setting, too.
# With the lp-filter 10Hz really is the lowest we can go to still get the full amplitude of the oscillations

# block_no = 2 # 1 #
# segment_no = 0
# time_slice = [80, 120]  # [200, 250] #
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     min_depolspeed=0.15,
#                                     min_depolamp=0.2,
#                                     ahp_width_window=200,
#                                     noisefilter_hpfreq=3000,
#                                     oscfilter_lpfreq=10,
# )


# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.2,
#                                                      min_depolspeed=0.15,
#                                                      ahp_width_window=200,
#                                                      noisefilter_hpfreq=3000,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# 1. seeing that light/puff-evoked things all got labeled as such
# notes:
# no TTL-evoked events recorded in this experiment.


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
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )



















# %% analyses done on events>3mV only
# %% plots: seeing that depolarizing events got extracted nicely
# des_df = singleneuron_data.depolarizing_events
#
# # 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# # notes:
#
#
# # 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# # singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# # notes:
#
#
# # Let's see some events, and their amplitude and rise-time to narrow down from there:
# probably_neatevents = (des_df.file_origin == 'gapFree_0001.abf') & (des_df.peakv_idx < 11400000)
# possibly_spontfastevents = (possibly_spontfastevents & probably_neatevents)
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# nbins = 20
# possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
#
