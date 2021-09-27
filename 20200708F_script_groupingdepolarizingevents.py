# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200708F'
singleneuron_data = SingleNeuron(neuron_name)
nbins = 100
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# a super relevant recording: Thy1-evoked excitations, also with application of AP5
# there's about 15 min. of recording without blocker, and then almost an hour with;
# early on, the neuron is mostly just going in and out of oscillating (small and large amp), but
# later on it starts doing spikes and fast-events vigorously.
# !Note: it's the cell that just won't die, but that doesn't mean its unaffected by drift - there are periods where
# it's definitely not all that healthy, and bridge issues etc. may be playing up.
# Also, it has lots of events that are clearly compound (double peaks, wider than single events).
# !! They tend to get picked up as a single event by the algorithm, should consider that when calculating frequency.

# summary plots:



# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# Seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# This looks alright - the upstrokes of the evoked events are usually quite compound and baselinepoints aren't
# always perfect, but there definitely shouldn't be any contamination of spont.events with evoked ones so I'm happy.

# Seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# possibly_spontfastevents = (spont_events & unlabeled_events)
# %%
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# Looking quite alright from the perspective of events getting picked up: definitely everything that's 2mV or larger
# got listed. My eyes did pick out some double-events though, where not the first but only the second peak got labeled
# (and the baseline-point can be off). This'll be interesting to tease apart...

# 1. my first run of going at labeling fast-events - really just filtering out some compound ones
# Let's see amplitude and rise-time distributions to narrow down from there:
# The amplitude histogram shows groups of events 5mV or larger; smaller events are just too numerous to say anything.
# But also in events with amp>5mV there seems to be significant variance in rise-time.
# Let's see only events >5mV to start with:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 5) & (des_df.amplitude < 15))
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=60)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=20,
#                                    plot_dvdt=True
#                                    )
# OK then, lots of things going on there... I'm sure some of them are classic fast-events, others are double-events,
# and then there's events with fast rise but different decay than the fast-events (and those come as doubles, too).

# Let's see their widths also, maybe it'll be easier to select them based on that:
# possibly_spontfastevents_df.hist(column=['width_30', 'width_50', 'width_70'], bins=60)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )

# Looks like there's a clear break in the width_50 histogram at 7ms, and just a handful events wider than that -
# let's see them:
# probably_notfastevents = (possibly_spontfastevents & (des_df.width_50 > 7))
# I don't think these are fast-events (they're too round and wide and variable in their normalized decay waveform),
# but they are definitely events of some sort... not labeling them for now.

# Let's instead work our way through the events by rise-time, starting from the slowest ones.
# Compound events are easy to recognize by eye by the kink in the rise, let's at least filter those out first.
# Starting from the slowest-rising events:
# probably_notfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 1.6))
# these are all compound events with a kink in their rise. Labeling them as such:
# compound_events = probably_notfastevents
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Now let's see events with slightly faster rise:
# probably_notfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 1))
# These are all compound events, except for three that are simply rather wide.
# Let's get histograms of width and see if we can tell them apart:
# yes, looks like there's always three that are wider than all the others.
# Let's see that we get compound-events only:
# probably_compoundevents = (probably_notfastevents & (des_df.width_50 > 5))
# singleneuron_data.plot_depolevents(probably_compoundevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# The smallest of these events in fact has a simple rise, the rest are clearly compound with a kink in the rise.
# Labeling them as such:
# compound_events = (probably_compoundevents & (des_df.amplitude > 7))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Let's see the next batch of events with again slightly faster rise:
# probably_notfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 0.9))
# Looks like the two events with the narrowest width are compound events with a clear kink in the rise:
# compound_events = (probably_notfastevents & (des_df.width_70 < 2))
# singleneuron_data.plot_depolevents(compound_events,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# Indeed. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Let's see the next batch of events with again slightly faster rise:
# probably_notfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 0.8))
# In this group there is just one event with a clear kink in the rise, clearly separable from other events by amp.
# Labeling it as such:
# compound_event = (probably_notfastevents & (des_df.amplitude > 13) & (des_df.amplitude < 17))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Let's see the next batch of events with again slightly faster rise:
# probably_notfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 0.6)
#                           & (des_df.rise_time_20_80 < 0.9))  # we've examined those already
#
# singleneuron_data.plot_depolevents(probably_notfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=20,
#                                    timealignto_measure='rt20_start_idx',
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_depolevents(probably_notfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    plotwindow_inms=20,
#                                    timealignto_measure='rt20_start_idx',
#                                    plot_dvdt=True,
#                                    )
# probably_notfastevents_df = des_df[probably_notfastevents]
# probably_notfastevents_df.hist(column=['width_30', 'width_50', 'width_70'], bins=60)
#
# # Let's see how these events evolve over the course of recording, by color-coding them by time:
# singleneuron_data.plot_depolevents(probably_notfastevents,
#                                    colorby_measure='peakv_idx',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=20,
#                                    timealignto_measure='rt20_start_idx',
#                                    plot_dvdt=True,
#                                    )
# Yup, that looks like the neuron starting to do funnier things with increasing time.

# probably_notfastevents = (possibly_spontfastevents
#                           & ((des_df.width_50 > 7) | (des_df.rise_time_10_90 > 1.2))
#                           )
# possibly_spontfastevents = (possibly_spontfastevents
#                           & ~((des_df.width_50 > 7) | (des_df.rise_time_10_90 > 1.2))
#                           )
# singleneuron_data.plot_depolevents(probably_notfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# OK, now it's starting to get clearer what are fast-events. The problem is that some of them are compound and therefore
# have a break in the upslope, which gives them longer rise-time and width; and then the rounder events are just quite
# variable in all of amp, rise and width so that the distributions bleed into each other really badly.
# %%
# 2. starting a new run of labeling fast-events in this neuron, having worked on a bunch of other (more and less
# canonical) examples in between...

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
# 3. As usual, let's start with the largest amplitude group - there's a handful of events here that have surprisingly
# high amplitude (20 - 40mV) that should be examined and labeled. Let's see them alongside some other events that are
# more likely to be fast-events:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 10))
# 3a. the largest three of these events are clearly compound (from looking at the dvdt plot):
# compound_events = (unlabeled_spont_events & (des_df.amplitude > 20))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 3b. in the now remaining events, the ones with the most depolarized baselinev are compound:
# compound_events = (events_underinvestigation & (des_df.baselinev > -38))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 3c. of the remaining events only one is clearly compound, the rest just look kinda noisy (two of them especially are
# particularly wide, but checking them in the raw data trace it's clear that this happens at a time where the neuron is
# getting leaky and unhappy).
# compound_event = (events_underinvestigation & (des_df.baselinev > -40.65) & (des_df.baselinev < -40.5))
# fastevents = (events_underinvestigation & ~compound_event)
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 4. moving on to the next amplitude group: events with amp >= 8mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 8))
# I don't see any compound events here, just once again some that are more noisy than others (including two that are
# particularly wide, just like in the previous amplitude group)
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 5. moving on to the next amplitude group: events with amp >= 5mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 5))
# there are two events in there that are clearly compound from their dvdt/V-plot shape: the single widest one, and the
# largest one of those occurring at more hyperpolarized baselinev:
# compound_event1 = (events_underinvestigation & (des_df.width_50 > 8))
# compound_event2 = (events_underinvestigation & (des_df.amplitude > 7.5) & (des_df.baselinev <= -40))
# compound_events = (compound_event1 | compound_event2)
# fastevents = (events_underinvestigation & ~compound_events)
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 6. moving on to the next amplitude group: events with amp >= 2.5
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 2.5))
# 6a. the event occurring at the most depolarized baselinev (>-20) is a compound one of which only the second peak got
# picked up; labeling it as compound event:
# compound_event = (events_underinvestigation & (des_df.baselinev > -20))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 6b. in the remaining events there's mostly fast-events, but also a handful of compound events and large spikelets (or
# possibly they are just noise-things - either way they're much wider and not shaped like fast-events at all).
# not_fastevents = (events_underinvestigation & ((des_df.width_50 > 6) | (des_df.width_50.isna())))
# having looked at all remaining events individually there are just two that are clearly compound, the rest look like
# they are single fast-events.
# compound_events = (events_underinvestigation & ~not_fastevents & (des_df.rise_time_20_80 > 1.2))
# fastevents = (events_underinvestigation & ~(not_fastevents | compound_events))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 7. finally, looking at all remaining events there is a small group (6 events) that stands out in the
# rise-time/maxdvdt scatter
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.14))
# - they are definitely fast-events (one or two may be compound, but not definite enough to say). This makes me think
# that there may be more fast-events among the smaller things, too... Let's just see any events with maxdvdt >- 0.08 -
# at lower values of maxdvdt the distribution looks normal, and by setting this as a cutoff value we should definitely
# be catching anything that could obviously be a fast-event.
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.08))
# Definitely lots of fast-events in this group, but also some outliers and perhaps even some distincly compound events.
# First, events with rise-time > 1.2 (break in the histogram there) are not fast-events, or at least not clearly
# recognizable as such because they're in too noisy a stretch of recording.
# other_events = (events_underinvestigation & (des_df.rise_time_20_80 > 1.2))
# events_underinvestigation = (events_underinvestigation & ~other_events)
# It's taken some convincing myself, but having seen the remaining events within the context of the raw data trace I'm
# actually pretty sure that these are all fast-events. Labeling them:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# # %%
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

# I will not claim that all fast-events were labeled, especially since they seem to get very small. But I think I
# labeled everything that can in good conscience be called a fast-event: the distributions of the remaining events'
# parameters all look rather normal with a long-ish tail towards higher values, as I would expect from a collection of
# spikelets and regular synaptic depolarizations.


#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
