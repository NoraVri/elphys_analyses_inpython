# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190331A1'
singleneuron_data = SingleNeuron(neuron_name)
nbins = 100

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
probably_spikelets = (unlabeled_spontevents & (des_df.amplitude < 1.7) & (des_df.maxdvdt < 0.12))  # see plots and analyses section3

# %% summary plots:
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
des_df[probably_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
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

# scatters of events parameters:
# fast-events
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
# %% plots for publication figures:
nbins = 100  #
# neat single fast-events:  # see plots and analyses section7
probably_neatevents = ((des_df.file_origin == 'gapFree_0000.abf')
                       & (des_df.peakv_idx > 12100000)  # gapFree_0 trace starts at t=1075s, gets good at t=1680s, so after idx=12100000
                       & (des_df.baselinev < -30)  # filters out events that look not so neat
                       )
# %%
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
# %%
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
des_df = singleneuron_data.depolarizing_events

# seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# neuron deteriorates badly over the course of recordings, with conditions sometimes changing rather abruptly.
# It'll be worth going over the data file-by-file to clear out 'bad' events occurring during specific stretches of recordings

# 1. Let's see distributions of events parameters and start narrowing down from there:
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
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







# Let's see if the fast-events occurring during the neatest stretch of recordings will indeed look like
# neat fast-events:
# fast_events = des_df.event_label == 'fastevent'
# probably_neatevents = ((des_df.file_origin == 'gapFree_0000.abf')
#                        & (des_df.peakv_idx > 12100000)  # gapFree_0 trace starts at t=1075s, gets good at t=1680s, so after idx=12100000
#                        & (des_df.baselinev < -30))  # filters out one event that's sitting on a +DC current pulse
# singleneuron_data.plot_depolevents((fast_events & probably_neatevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# des_df[(fast_events & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',],
#                                                  bins=nbins)
# the amplitude grouping is still not very clear, but it seems like there could be two main peaks very close together (6.2 and 6.7 mV).
# Other than that, these are beautiful fast-events with identical decay shape, width correlating with baselinev.

# Now just for the hell of it, I want to see neat compound-events and see how their distributions fit with the
# single fast-events:
# singleneuron_data.plot_depolevents((compound_events & probably_neatevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    )
# des_df[(compound_events & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',],
#                                                  bins=nbins)
# interesting - indeed it looks like the compound fast-events could be just two single events stacked, but it's
# noteworthy that the maxdvdt of the compound events is much higher (mostly ~1, up to 1.7) than of the single events
# (~0.45 on avg, pretty normal-looking distribution between 0.3 and 0.6).