# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190401B1'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# quite nice recording, neuron holding very steady for the most part (until shortPulse, where it starts to lose
# baselinev pretty badly). It's oscillating throughout, small-amp wacky; occasionally this affects the decay of
# fast-events, but mostly they seem to be riding on top without being affected much.
# Neuron has a lot of spont.APs (especially early on), and they all look to be evoked from a fast-event (10mV,
# not one that we see often on its own).

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section3
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section3a
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  # no TTL-applied experiments in this neuron
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents

# %% summary plots - all events:
# histogram of baselinev in the entire recording:
singleneuron_data.get_timespentrecording(make_baselinev_hist=True)  # takes very long to make
nbins = 100
# histograms of events parameters
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
plt.suptitle('probably-spikelets parameter distributions')

# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots of the main events-groups (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   )
# fastevents
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=12,
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
baselinevgroup1 = (des_df.baselinev < -48)
baselinevgroup2 = (des_df.baselinev > -44)
# ampgroup1 = (fastevents & neat_events & (des_df.amplitude < ))
# ampgroup2 = (fastevents & neat_events & (des_df.amplitude > ) & (des_df.amplitude < ))
# ampgroup3 = (fastevents & neat_events & (des_df.amplitude > ) & (des_df.amplitude < ))
# ampgroup4 = (fastevents & neat_events & (des_df.amplitude > ) & (des_df.amplitude < ))
# ampgroup5 = (fastevents & neat_events & (des_df.amplitude > ))
#
# # fast-events normalized
singleneuron_data.plot_depolevents((fastevents & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events, normalized'
                                   )
# # fast-events normalized, averaged per baselinev group
singleneuron_data.plot_depoleventsgroups_averages((fastevents & neat_events & baselinevgroup1),
                                                  (fastevents & neat_events & baselinevgroup2),
                                                  group_labels=['low baselinev', 'high baselinev'],
                                                  plotwindow_inms=20,
                                                  do_normalizing=True,
                                                  )
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
# %% plots: subtracting single events from compound ones


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# overall a quite nice and stable-looking recording (no -DC applied anywhere to keep baselinev) except towards
# the very end (shortPulse 01) where baselinev deteriorates badly. Also, it seems like fast-events frequency is
# going down over time, disappearing to almost 0 after about 45 minutes of recording.

# I will use gapFree_0000 for extracting depolarizing events, as this is the trace with the most fast-events in it.
# the neuron's oscillations are nicely captured by a 10Hz lp-filter; AHP width window increased to 200ms because 150ms
# often cuts it too close; min_depolspeed increased to 0.2mV/ms because below that there's really just noise (from seeing the event-detect-trace derivative).

# block_no = 0
# segment_no = 0
# time_slice = [400, 500]  # [800, 950]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                                     min_depolamp=0.1,
#                                                     oscfilter_lpfreq=10,
#                                                     ahp_width_window=200,
#                                                     min_depolspeed=0.2,
#
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.1,
#                                                      min_depolspeed=0.2,
#                                                      ahp_width_window=200,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()


# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=3)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# 1. seeing that light/puff-evoked things all got labeled as such
# notes:
# no ttl-evoked events recorded in this experiment.

# 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# looking good. It's very clear that fast-events are numerous earlier on in the recording, and they almost completely
# stop occurring after ~45 min. (as do spont.APs).

# plotting events parameters:
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# From these distributions, it looks like it should be relatively easy to find all the fast-events: amplitude,
# maxdvdt and rise-time seem to delineate the groups (fast-events vs slow events) quite nicely.
# let's see these parameters in a single plot:
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='maxdvdt',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# yea that makes it pretty clear - in the events up to 1.5mV amplitude we won't find any fast-events;
# at amplitudes above that there's a group of events with very fast rise-time (~0.5ms) and a few outliers that I'm
# not sure yet what they are.

# 3. Let's see events and parameters of everything with amp>1.5mV:
# events_under_investigation = (unlabeled_spont_events & (des_df.amplitude > 1.5))

# The events with amp>4mV all look pretty neatly like fast-events, though there may be a few compound ones in there
# as well. The events with amp <4mV are mostly noise-things, and two events that look faster and sharper than anything
# else. I'll start with seeing all the larger events, and fishing out the doubles from among there:
# events_under_investigation = (unlabeled_spont_events & (des_df.amplitude >= 4))
# 3a. that's still quite a lot of events, need to split them out to see clearly.
# The one event occurring at depolarized baselinev (>-40) is a compound event. Labeling it:
# singleneuron_data.depolarizing_events.loc[(events_under_investigation & (des_df.baselinev > -40)),
#                                           'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 3b. Now let's see events with baselinev < -44mV:
# the single largest event in there (>12mV) is a compound one, otherwise all events look like single fast-events
# (there's a few that may have a small pre-potential, but there are no outliers by parameter values so leaving that be).
# Labeling them:
# compound_events = (events_under_investigation & (des_df.baselinev < -44) & (des_df.amplitude > 12))
# fastevents = (events_under_investigation & (des_df.baselinev < -44) & (des_df.amplitude < 12))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3c. the remaining events in this group are all clearly fast-events, with rise-time, maxdvdt and width looking like
# pretty neat Gaussian distributions. There are two events that have much smaller maxdvdt (~0.15mV/ms) than the rest
# (0.3-0.7mV/ms), but these turn out to be on depolarizing current steps in the IV protocols and their normalized
# waveform is exactly like the other fast-events. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[events_under_investigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3d. now let's see the last few remaining events of amp > 1.5:
# Three of these 5 events are noise-things: two have impossibly short rise-time, and the third is a wobble in baselinev
# occurring early on. The other two may not be very 'neat' events (occurring late in the recordings at rather
# depolarized baselinev) but they do look like fast-events. Labeling them:
# fastevents = (events_under_investigation & (des_df.rise_time_20_80 > 0.5) & (des_df.rise_time_20_80 < 2))
# noiseevents = (events_under_investigation & (~fastevents))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# plotting events parameters:
# des_df[events_under_investigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=events_under_investigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=events_under_investigation,
#                                                       )
# # plotting events:
# singleneuron_data.plot_depolevents(events_under_investigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

#### this concludes sorting through all fast-events and labeling them ####

# %% selecting 5 minutes of best typical behavior and marking 'neat' events
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks('gapFree',
#                                      events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)

# 5 min. of recording from file gapFree_0000, from 635s to 935s  - 5 minutes with the largest AP amp, very steady despite some drop in baselinev
# block_name = 'gapFree_0000.abf'
# window_start_t = 635
# window_end_t = 935
# sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
# trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices'][block_name]['t_start']
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

# %%

