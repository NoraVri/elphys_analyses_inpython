# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190331A1'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# oscillating neuron that didn't get patched properly and was deteriorating badly for most of the recording; but
# even when held with -1nA DC towards the end of recordings it's still oscillating and doing fast-events and spikelets
# Since by eye, the (high) frequency of APs and other events does not seem affected much by recording conditions being
# un-ideal (at least initially), I'll be labeling 'degenerate' events by their proper names so they'll end up in the
# events-counts in the summary plots. The plots for publication will filter down to include only events from 'nice'
# stretches of recording.
# After seeing and labeling all events and finding a large group of 'nice' ones still no clear amplitude grouping is
# visible. However, it seems that there may be two groups very close together - 6.2 and 6.7mV amp - and that events of
# this size are often stacked into compound events.
# Also, the neuron oscillating does not seem to affect the decay shapes much at all, but intriguingly it does seem like
# there may be a phase relationship (though note that with small oscs, the large-amp events will create their own
# wobble in the lp-filtered trace, so should look very carefully into that).


des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section6
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section5
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  # no TTL-applied experiments in this neuron
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = (unlabeled_spontevents & (des_df.amplitude < 1.7) & (des_df.maxdvdt < 0.12))  # see plots and analyses section3

# %% summary plots - all events:
# histogram of baselinev in the entire recording:
singleneuron_data.get_timespentrecording(make_baselinev_hist=True)
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
plt.suptitle('probably-spikelets parameter distributions')

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

# %% summary plots: neat events only
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
baselinevgroup1 = (des_df.baselinev < -40)
baselinevgroup2 = (des_df.baselinev > -40)
ampgroup1 = (fastevents & neat_events & (des_df.amplitude < 3))
ampgroup2 = (fastevents & neat_events & (des_df.amplitude > 3) & (des_df.amplitude < 5.5))
ampgroup3 = (fastevents & neat_events & (des_df.amplitude > 5.5) & (des_df.amplitude < 6.5))
ampgroup4 = (fastevents & neat_events & (des_df.amplitude > 6.5) & (des_df.amplitude < 7.5))
ampgroup5 = (fastevents & neat_events & (des_df.amplitude > 7.5))

# fast-events normalized
singleneuron_data.plot_depolevents((fastevents & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events, normalized'
                                   )
# fast-events normalized, averaged per baselinev group
singleneuron_data.plot_depoleventsgroups_averages((fastevents & neat_events & baselinevgroup1),
                                                  (fastevents & neat_events & baselinevgroup2),
                                                  group_labels=['low baselinev', 'high baselinev'],
                                                  plotwindow_inms=20,
                                                  do_normalizing=True,
                                                  )

# fast-events averaged per amplitude group (sorted by eye), separately for 2 baselinev values
singleneuron_data.plot_depoleventsgroups_averages((ampgroup1 & baselinevgroup1),
                                                  (ampgroup2 & baselinevgroup1),
                                                  (ampgroup3 & baselinevgroup1),
                                                  (ampgroup4 & baselinevgroup1),
                                                  (ampgroup5 & baselinevgroup1),
                                                  group_labels=['group1', 'group2', 'group3', 'group4', 'group5'],
                                                  plotwindow_inms=20,
                                                  plt_title='baselinev < -40mV'
                                                  )
singleneuron_data.plot_depoleventsgroups_averages((ampgroup1 & baselinevgroup2),
                                                  (ampgroup2 & baselinevgroup2),
                                                  (ampgroup3 & baselinevgroup2),
                                                  (ampgroup4 & baselinevgroup2),
                                                  (ampgroup5 & baselinevgroup2),
                                                  group_labels=['group1', 'group2', 'group3', 'group4', 'group5'],
                                                  plotwindow_inms=20,
                                                  plt_title='baselinev > -40mV'
                                                  )

# %% plots: subtracting single events from compound ones
# compound_event = (compound_events & probably_neatevents & baselinevgroup1 & (des_df.baselinev > -44))
compound_event = (compound_events & neat_events
                  & (des_df.baselinev < -44) & (des_df.baselinev > -44.9))
singleneuron_data.plot_depoleventsgroups_averages(compound_event, (ampgroup5 & baselinevgroup1),
                                                  group_labels=['compound event', 'single event'],
                                                  subtract_traces=True,
                                                  delta_t=-0.85,
                                                  plotwindow_inms=20)

# interesting - indeed it looks like the compound fast-events could be just two single events stacked, but it's
# noteworthy that the maxdvdt of the compound events is generally much higher (mostly ~1, up to 1.7) than of the
# single events (~0.45 on avg, pretty normal-looking distribution between 0.3 and 0.6).
# %%
# selecting a short piece of recording (~2min) to compare single and double events occurring there
selected_events = ((des_df.file_origin=='gapFree_0000.abf')
                   & (des_df.peakv_idx > (20000 * (2119 - singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices']['gapFree_0000.abf']['t_start']))))

compound_event = (compound_events & selected_events
                  & (des_df.baselinev < -36.25))
single_events = (fastevents & selected_events
                 & (des_df.baselinev < -36.25) & (des_df.maxdvdt > 0.4))

singleneuron_data.plot_depoleventsgroups_averages(compound_event, single_events,
                                                  group_labels=['double event', 'single events'],
                                                  timealignto_measure='rt20_start_idx',
                                                  plotwindow_inms=15,
                                                  subtract_traces=True,
                                                  delta_t=-0.25
                                                  )
# %%
compound_event = (compound_events & selected_events
                  & (des_df.baselinev > -34))
single_event = (fastevents & selected_events
                 & (des_df.amplitude > 8) )
singleneuron_data.plot_depoleventsgroups_averages(compound_event, single_event,
                                                  group_labels=['double event', 'single event'],
                                                  timealignto_measure='rt20_start_idx',
                                                  plotwindow_inms=15,
                                                  subtract_traces=True,
                                                  delta_t=-0.195
                                                  )
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# picked a time-slice of 'best typical behavior' to check whether all events (also small spikelets)
# get extracted nicely with default settings - not exactly:
# Looks to me that 'events' of ~0.1mV are pretty much indistinguishable from wobbles in the voltage - not just for the algorithm but also by eye.
# Also, the 20Hz high-pass filter can be taken down, the cell never oscillates that fast.
# Decreasing depol_to_peak_window gets rid of some of the more noise-looking 'events' (amp up to 0.3mV)


# block_no = 0
# segment_no = 0
# time_slice = [1750, 1800]
# #
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     min_depolamp=0.2,
#                                     depol_to_peak_window=4,
#                                     # event_width_window=40,
#                                     oscfilter_lpfreq=10,
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.2,
#                                                      depol_to_peak_window=4,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()


# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events

# seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# neuron deteriorates badly over the course of recordings, with conditions sometimes changing rather abruptly.
# It'll be worth going over the data file-by-file to clear out 'bad' events occurring during specific stretches of recordings

# 1. Let's see distributions of events parameters and start narrowing down from there:
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# Well, it's clear that there's small (amp < ~2mV) and large (amp up to 50mV) events - this is very clear also in
# the amp/rise-time scatter, even though the amplitudes and rise-times of the large events are also all over the place.

# 2. Let's first see the group of events with amp > 30mV - my feeling is they are all degenerate APs occurring early on
# in the recording (started from spont.break-in with recording conditions improving initially, reaching a really nice
# steady-state after ~30min)
# hugeamp_events = (possibly_spontfastevents & (des_df.amplitude > 30))
# des_df[hugeamp_events].file_origin - indeed, they're all from that first stretch where we see degenerate-looking APs:
# singleneuron_data.plot_rawdatablocks('gapFree_0000', events_to_mark=hugeamp_events)
# labeling the events as APs:
# singleneuron_data.depolarizing_events.loc[hugeamp_events, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()

# 3. Next, let's see the group of small events, as delineated by maxdvdt and amp (the grouping looks just a little bit
# clearer to me there than by rise-time)
# probably_smallslowevents = (possibly_spontfastevents & (des_df.maxdvdt < 0.12) & (des_df.amplitude < 1.7))  # cutoff values chosen to fall well within 'empty areas'
# probably_smallslowevents_df = des_df[probably_smallslowevents]
# probably_smallslowevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_smallslowevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_smallslowevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_smallslowevents,
#                                                       )
# let's see the larger ones of these events to see if maybe they would clearly not be spikelets:
# singleneuron_data.plot_depolevents((probably_smallslowevents & (des_df.amplitude > 1)),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=15)
# yea that all looks very spikelet-ey to me, definitely too noisy to say for certain that they could be fast-events.

# 4. So let's update our definition of possibly_spontfastevents in this neuron, and see what we're left with:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.maxdvdt > 0.12) & (des_df.amplitude > 1.7))
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# nbins = 300  # even dividing ~900 events into this many bins, most of them have rise-time distributed very narrowly around 0.5ms
# possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )

# Interestingly, there seems to be a pretty clear grouping both in the rise-time/amp and in the rise-time/width scatters,
# with one group having pretty tight parameter ranges (amp 3-10mV, rise-time 0.2-0.6ms) and the other having
# rise-time>0.7 and much wider amplitude distribution (up to 25mV).
# Now, from what I saw in the rawdata traces, this neuron may have quite a lot of compound events, which could explain
# these distributions. Let's see:
# probably_compoundevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 0.7))  # cutoff value chosen based on the tight group seen in the rise-time/amp scatter
# probably_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 <= 0.7))
# singleneuron_data.plot_depolevents(probably_compoundevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=15
#                                    )
# singleneuron_data.plot_depolevents(probably_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=15
#                                    )
# Indeed, that looks like a pretty good division - I'm quite sure that none of the events in probably_spontfastevents
# could be said to be compound, and it looks like practically all of the events in probably_compoundevents are indeed
# that - except maybe for a handful of relatively small (amp~4mV), broad-ish events that I'm not sure right now what they're supposed to be).

# 5. Let's see the groups of compound events in a little more detail, and label the ones that are for sure that:
# probably_compoundevents_df = des_df[probably_compoundevents]
# probably_compoundevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                          'baselinev', 'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
# I don't see a clear grouping by any measure, so I'm just gonna go by recording files:
# actually that didn't help much - it seems all but a dozen or so compound-events occur in the first 20min of recordings.
# singleneuron_data.plot_depolevents((probably_compoundevents
#                                     # & (des_df.file_origin == 'gapFree_0000.abf')
#                                     & (des_df.amplitude <= 10)
#                                     ),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=15,
#                                    # plt_title='gapFree_0000'
#                                    )
# The larger events (amp > 10mV) are clearly all compound, no doubt from looking at this plot (and the normalized one)
# In the smaller events (amp <= 10mV) there's one 10mV one occurring at highly depolarized membrane potential (it's
# sitting on a +DC current pulse) and a handful smaller ones that look like they're not in fact compound.
# Let's see if this is reflected in the parameter distributions:
# mixed_events = (probably_compoundevents & (des_df.amplitude <= 10))
# des_df[mixed_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
# looks like rise-time and width delineate the handful of non-compound events nicely:
# singleneuron_data.plot_depolevents((probably_compoundevents
#                                     & (des_df.amplitude <= 10)
#                                     & (des_df.rise_time_20_80 <= 1)
#                                     & (des_df.width_30 < 6.5)),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# by their short rise-time and large amplitude these are all fast-events, let's label them as such:
# fast_events = (probably_compoundevents & (des_df.amplitude <= 10) & (des_df.rise_time_20_80 <= 1) & (des_df.width_30 < 6.5))
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# As for the remaining compound events, it's clear that they are indeed compound. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[probably_compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# 6. Now let's return to the fastevents, see them in detail and label where appropriate:
# probably_spontfastevents_df = des_df[probably_spontfastevents]
# probably_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                          'baselinev', 'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
# interestingly, the maxdvdt/amplitude scatter clearly shows two distinct groups, with one having generally much smaller
# maxdvdt and higher baselinev than the other. I suspect it's a matter of the recording quality, let's see:
# group1fastevents = (probably_spontfastevents & (des_df.maxdvdt < 0.25) & (des_df.baselinev > -45))
# group2fastevents = (probably_spontfastevents & ~group1fastevents)
#
# singleneuron_data.plot_depolevents((group1fastevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# des_df[group1fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
#
# singleneuron_data.plot_depolevents((group2fastevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# des_df[group2fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)

# both groups look like fast-events, with very short rise-time (0.4 - 0.7ms)
# singleneuron_data.plot_rawdatablocks(events_to_mark=group1fastevents, segments_overlayed=False)
# singleneuron_data.plot_rawdatablocks(events_to_mark=group2fastevents, segments_overlayed=False)
# the division isn't perfect, but the group1 events all occur later on in the recording where conditions deteriorate,
# and accordingly they are generally a bit wider (on avg. ~3.5ms half-width) and have smaller maxdvdt (up to ~0.2).
# Group2 events occur mostly during the first half hour (only a handful are elsewhere), have half-width of 2-4ms and
# would be almost perfect examples of fast-events except that the decay-shape gets slower for some events occurring at
# more hyperpolarized baselinev.
# Anyway, let's label all these events as fast-events:
# singleneuron_data.depolarizing_events.loc[probably_spontfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 7. Now let's return again to all as-yet unlabeled events and see if anything stands out:
# Indeed, there are still quite a few pretty large amp (up to 14mV) events that haven't gotten labeled yet; we missed
# them before because their maxdvdt is just a little smaller than 0.12mV/ms (more like 0.1). From the amp/maxdVdt
# scatter it's clear that there is a group of small events (amp up to 1.5mV) and then larger events; looking at
# where these are in the raw data it's clear that the larger of these events all occur later on during recordings
# (IV files). Also, the one >2mV 'event' occurring in the shortPulse file is a noise-thing. Labeling it as such:
# noiseevent = (possibly_spontfastevents & (des_df.amplitude > 1.5) & (des_df.file_origin == 'shortPulse_0000.abf'))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# Now let's see the two groups of remaining events to confirm they are what I think they are:
# probably_spikelets = (possibly_spontfastevents & (des_df.amplitude <= 1.5))
# des_df[probably_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
# yea, that looks very neatly like parameter distributions we'd expect from spikelets
# probably_fastevents = (possibly_spontfastevents & (des_df.amplitude > 1.5))
# singleneuron_data.plot_depolevents((probably_fastevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# des_df[probably_fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
# indeed these all look like fast-events, though quite a lot of them are compound. Definitely all the larger ones
# (>6mV) are compound, let's label those first:
# compound_events = (possibly_spontfastevents & (des_df.amplitude > 6))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# In the remaining events we have just a single compound one, the one with the longest rise-time by far (almost 2ms,
# fast-events mostly 0.6-1ms). Labeling the events:
# compound_event = (probably_fastevents & (des_df.rise_time_20_80 > 1.5))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# fastevents = (probably_fastevents & (des_df.rise_time_20_80 < 1.5))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### this concludes sorting through all events and labeling them ####

# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks(
#                                      events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)
# notes:
# not a great recording initially, but it improves over the first half hour of recordings and stays stable for quite
# a while there; even if resting at baselinev ~-35mV, it seems quite happy, oscillating a bit and firing off lots of
# fast-events, double-events and APs. It is losing restingV steadily over the course of recordings, with noticeable
# impact on oscs and AP amp starting from file IV_0002. So, selecting the second part of gapFree_0000 and the first
# two IV-files as stable recording time. However, upon closer inspection it is clear that the recording is deteriorated
# already in the IV files: the divide is really clear, with fast-events in gapFree_0000 reaching at least
# 0.3mV/ms maxdVdt while fast-events occurring during IV files barely reach 0.2mV/ms. So, labeling only events from
# the first file as neat:

# second part of gapFree_0000, starting from 1680s in
sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices']['gapFree_0000.abf']['t_start']
neat5min_start_idx = (1680 - trace_start_t) * float(sampling_frequency)
probably_neatevents = ((des_df.file_origin == 'gapFree_0000.abf')
                       & (des_df.peakv_idx > neat5min_start_idx)  # gapFree_0 trace starts at t=1075s, gets good at t=1680s, so after idx=12100000
                       )
# the IV files
# probably_neatevents2 = ((des_df.file_origin == 'IV_0000.abf') | (des_df.file_origin == 'IV_0001.abf'))
# probably_neatevents = (probably_neatevents1 | probably_neatevents2)

# plotting the neat events in the raw data trace to confirm labeling:
# singleneuron_data.plot_rawdatablocks(*des_df[((fastevents | compound_events)
#                                               & probably_neatevents)].file_origin.unique(),
#                                      events_to_mark=((fastevents | compound_events) & probably_neatevents),
#                                      segments_overlayed=False)

# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()

# %% marking 'n neat fast events': the first 10 - 20 events to occur during stable recording at resting baselinev
# fastevents = ((des_df.event_label == 'fastevent') & (des_df.neat_event)) & (des_df.baselinev > -40)
# neatevents = fastevents.copy()
# neatevents[neatevents] = False
# fastevents = fastevents[fastevents]
# n = 19  # N - 1 (0-based indexing)
# i = 0
# # check that these events occur during resting baselinev
# for idx, value in fastevents.iteritems():
#     if i <= 19:
#         neatevents[idx] = True
#         i += 1
#     else:
#         break
# neatevents.name = 'n_neat_fastevents'
# adding the neatevents-series to the depolarizing_events-df:
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neatevents)
# singleneuron_data.write_results()
# %% plots and analyses: seeing APs and labeling fast-event triggered ones
# this neuron's got tons of APs with a double or even triple up-stroke; not sure what to do with that.
# Probably should first look at the double-events: in this neuron they look like they're composed of two differently
# shaped events (fast-event then AIS activation?).

# Let's first see the neat double events at hyperpolarized baselinev, and see if we can subtract single fast-events
# from them to get another single fast-event:
double_events = (compound_events & neat_events & (des_df.baselinev < -40))
single_events = (fastevents & neat_events & (des_df.baselinev < -40))

singleneuron_data.plot_depolevents((double_events | single_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat events'
                                   )
# %%
double_event1 = (double_events & (des_df.baselinev > -44))
single_events1 = (single_events & (des_df.maxdvdt >= 0.54) & (des_df.maxdvdt <= 0.56))

singleneuron_data.plot_depoleventsgroups_averages(double_event1, single_events1,
                                                  group_labels=['compound event', 'single event'],
                                                  subtract_traces=True,
                                                  delta_t=-1.8,
                                                  plotwindow_inms=20)