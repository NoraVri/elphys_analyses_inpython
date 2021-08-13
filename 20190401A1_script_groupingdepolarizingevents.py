# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190401A1'
singleneuron_data = SingleNeuron(neuron_name)
nbins = 200
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# quite a nice recording for the entire duration, not too much variability in recording conditions or cell health.
# Neuron is oscillating throughout with small amp (1 - 3mV) wacky oscillations, and has LOADS of fast-events all
# the time, though frequency does seem to decrease a bit as recording continues.


des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section2-4
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section2a-3
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  # no TTL-applied experiments in this neuron
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
# probably_spikelets - see plots and analyses section4

# summary plots:
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
# des_df[probably_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('probably-spikelets parameter distributions')

# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots:
# the main events-groups (aps, fastevents, compound events) together in one plot
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   )
# fast-events:
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=12,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

# %% plots for publication figures:
# neat single events: let's see events occurring in gapFree_0001, <550s in (after that there's some noise in the recording)
probably_neatevents = ((des_df.file_origin == 'gapFree_0001.abf') & (des_df.peakv_idx < (550 * 20000)))

singleneuron_data.plot_depolevents((fastevents & probably_neatevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events'
                                   )
des_df[(fastevents & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                        'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                                 bins=nbins)
plt.suptitle('fast-events, neat ones only')
# neat compound fast-events:
singleneuron_data.plot_depolevents((compound_events & probably_neatevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat compound events'
                                   )
des_df[(compound_events & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                                 bins=nbins)
plt.suptitle('compound events, neat ones only')



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
# seeing that light/puff-evoked things all got labeled as such
# notes:
# no TTL-evoked events recorded in this experiment.


# 1. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# I'm not gonna say that ALL spikelets got picked up, but it looks really damn close... Definitely looks like
# fast-events all got picked up neatly.


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

# OK, it's clear from these distributions that there are LOTS of things that could be fast-events, but there's also
# some puzzling things in there.
# 1. First off there's a handful of events with amp>15, but from their rise-time I'm not sure what they are.
# Let's see:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 15))
# I see - all except one of these (the one happening at the lowest baselinev) are compound events, as seen in
# the dVdt/V-plot shape. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.baselinev >= -60)), 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[(events_underinvestigation & (des_df.baselinev < -60)), 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2. now in the remaining events, the rise-time/amplitude histogram sure looks like it's got mostly fast-events in it,
# especially with amps>4 - few outliers by rise-time. Let's see:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 4))
# indeed, these mostly look like fast-events, with at least a handful of compound events as well and then perhaps some
# noise-stuff too.
# 2a. Let's see if we can narrrow it down by rise-time:
# probably_not_fastevents = (events_underinvestigation & (des_df.rise_time_20_80 >= 0.9))
# singleneuron_data.plot_depolevents(probably_not_fastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# OK, those are all compound-events except for the one smallest thing that turned out to be a rebound Ca-spike
# (which occurs due to current pulse). Labeling as such:
# smallslowthing = (probably_not_fastevents & (des_df.amplitude < 5))
# singleneuron_data.depolarizing_events.loc[smallslowthing, 'event_label'] = 'currentpulsechange'
# compound_events = (probably_not_fastevents & (des_df.amplitude >= 5))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# 2b. Now let's see what remains of events with amp>4:
# Looks like these could all be 'simple' fast-events: rise-time for this group is from 0.3 - 0.9ms, and it looks like
# any variance may be mostly due to recording conditions changing (baselinev increasing for events with slower rise).
# But there's a LOT of events, so let's see the events split out in groups just to make sure:
# looking at (events_underinvestigation & (des_df.rise_time_20_80 >= 0.6)
# alright then... Looking at these individually it's clear from the dVdt/V plot that most of them are in fact compound
# - the big ones (8 - 13mV) are stacked fast-events, the small ones (~4-6mV) are preceded by something slower. And then
# there's a handful of events with amplitudes in between that, that are single. Labeling them:
# fastevents = (events_underinvestigation & (des_df.rise_time_20_80 >= 0.6)
#               & (des_df.amplitude > 6.8) & (des_df.amplitude < 9.2))
# compound_events = (events_underinvestigation & (des_df.rise_time_20_80 >= 0.6)
#               & (~fastevents))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# 2c. now looking at (events_underinvestigation & (des_df.rise_time_20_80 >= 0.5)
# I'm gonna call all these single events - there's three that are preceded by a slower pre-potential of 0.5-2mV, but
# this pre-potential amplitude is negligible compared to the amplitude of the fast-event and so doesn't seem to affect the rise-time measurement.
# Labeling them:
# fastevents = (events_underinvestigation & (des_df.rise_time_20_80 >= 0.5))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2d. now looking at (events_underinvestigation & (des_df.rise_time_20_80 > 0.4))
# too many events to see dV/dt shape clearly, splitting out further:
# (events_underinvestigation & (des_df.rise_time_20_80 > 0.4) & (des_df.maxdvdt > 0.4) - these are all very neat,
# single fast-events. Labeling as such:
# fastevents = (events_underinvestigation & (des_df.rise_time_20_80 > 0.4) & (des_df.maxdvdt > 0.4))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 2e. next split: (events_underinvestigation & (des_df.rise_time_20_80 > 0.4) & (des_df.maxdvdt > 0.3) - these are almost
# all very neat, except for one event that's getting another spikelet or something on its decay-phase; it's easy to
# find by width. Labeling the events:
# fastevents = (events_underinvestigation & (des_df.rise_time_20_80 > 0.4)
#               & (des_df.maxdvdt > 0.3) & (des_df.width_50 < 3.2))
# compound_events = (events_underinvestigation & (des_df.rise_time_20_80 > 0.4)
#               & (des_df.maxdvdt > 0.3) & (des_df.width_50 >= 3.2))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# now in events (events_underinvestigation & (des_df.rise_time_20_80 > 0.4)) we're left with only neat fast-events.
# Labeling them:
# fastevents = (events_underinvestigation & (des_df.rise_time_20_80 > 0.4))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2f. looking now at the parameter distributions of events_underinvestigation, their rise-time are all very narrowly
# distributed (0.35 - 0.4ms). So I'll go over them in groups by maxdvdt values instead, starting with maxdvdt > 0.8:
# (events_underinvestigation & (des_df.maxdvdt > 0.8) - there's one event there that gets a spikelet ~10ms after the
# peak, but it doesn't stand out by any parameters. So, labeling all of these as fast-events:
# fastevents = (events_underinvestigation & (des_df.maxdvdt > 0.8))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 2g. (events_underinvestigation & (des_df.maxdvdt > 0.6): all fast-events. There are two that look a bit wider than
# the rest, but looking at those individually (along with dVdt/V plot) doesn't show any clear signs of these being
# compound-events or otherwise excludable. So labeling them all as fast-events:
# fastevents = (events_underinvestigation & (des_df.maxdvdt > 0.6))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 2h. Looking over all remaining events (wiht amp>4mV) in groups I see none that stands out clearly (there's one more
# in there that has a spikelet on its decaying phase, but no measured parameters that would clearly separate it from
# the group). Labeling them all as fastevents:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3. Now let's move on to the smaller events. It's clear from every plot that up to 1mV amp we just have tons of things,
# so let's focus on events with amp>1.
events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 1))
# From the rise-time/amp scatter it would seem that there are just a
# dozen or two of events that don't fit with the cloud of small, slow things; it's even clearer when coloring
# for maxdvdt:
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='maxdvdt',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
# 3a. Let's see events with amp>1 and maxdvdt>0.1:
# Ok. The larger ones of these events (>2.8mV) are definitely all fast-events, below that it's more complicated.
# Also, there's a single compound event in there, the one happening at the most depolarized baselinev. Labeling as such:
# compound_events = (events_underinvestigation & (des_df.maxdvdt > 0.1) & (des_df.baselinev > -35))
# fastevents = (events_underinvestigation & (des_df.maxdvdt > 0.1) & (des_df.amplitude > 2.8) & (des_df.baselinev <= -35))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 3b. Now let's again see all events with amp>1 and maxdvdt>0.1 and their parameter distributions, to see if we can
# find criteria for fast-events only:
# events_underinvestigation = (events_underinvestigation & (des_df.maxdvdt > 0.1))
# well, these events may be somewhat messy, but no matter how I split them out I cannot convince myself that these are
# not all fast-events. Labeling them:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 4. Now in the events that remain there are still some with rather large amplitude (up to 4mV), much larger than
# what I tend to see for spikelets. Let's see events with amp>3 and determine what they could be:
# OK. Those are either spikelets, or an oscillation coming on in some other way - either way, they are
# definitely not fast-events.
# %%
# singleneuron_data.plot_depolevents((events_underinvestigation & (des_df.maxdvdt > 0.1)),
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    # newplot_per_event=True,
#                                    )

# %%
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='rise_time_20_80',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='amplitude',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )

#### this concludes sorting through all events and labeling them ####