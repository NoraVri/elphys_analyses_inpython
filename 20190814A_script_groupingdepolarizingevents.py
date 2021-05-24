# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190814A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Has fast-events for sure: three groups of amp 7, 8 and 10 mV. Only two examples in the largest two groups,
# but it's enough to make it very clear that the decay is the same.
# I looked for but did not find any events <2mV amp that would clearly be fast-events, too.
#!Note: there's one fast-event happening ~13s into gapFree_withBlockers_0000 - since new file is started
# at the time of solution change, blockers had not actually reached the bath yet.


# summary plots:
des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
fast_events = des_df.event_label == 'fastevent'
fast_events_df = des_df[fast_events]
fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.0 to find good parameter settings; playing with parameters was done elsewhere, using stored settings
# to re-create data table:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# notes:
# no such experiments performed on this neuron; it does have blockers (AP5+DNQX) applied for part of recordings.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# The fast-events that are clear by eye (4 - 10mV) definitely all got picked up correctly, as well as a LOT of
# smaller stuff - noise things, but also events of ~2mV that seem to have a compound rise. It's gonna be interesting
# to look for fast-events in the mess of smaller things, but the big ones are very clear and will help narrow it down.

# From the amp/rise-time scatter it's very clear that any events >6mV should be fast-events.
# Let's see them:
# fastevents_candidates = (possibly_spontfastevents & (des_df.amplitude > 6))
# singleneuron_data.plot_depolevents(fastevents_candidates,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    )
# Oh yea that's very clear - 3 amplitude groups (7, 8 and 10mV) with two examples each in the largest two groups
# and a handful of the smaller ones. Labeling them as fastevents:
# singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Now let's see if there are any events <6mV that are clearly fast-events:
# It really doesn't look like it. The amplitude/rise-time scatter does seem to show another group of events
# of about 1mV amp, but their rise-time is about twice as fast as the large fast-events found so far.
# Let's take a look at them anyway:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_10_90 < 2) & (des_df.amplitude > 1.5))
# These events are all fairly similar to each other, but clearly different from the fast-event we're looking for.

# Let's take a quick look at events with 0.3 < rise_time < 1 to make sure there aren't any clear fast-events there:
# possibly_spontfastevents = (possibly_spontfastevents
#                             & (des_df.rise_time_10_90 < 1) & (des_df.rise_time_10_90 > 0.3)
#                             & (des_df.amplitude > 0.5))  # below 0.5mV there's just too many events to make anything out
# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('spont. events, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (20-80%)')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (10-90%)')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# singleneuron_data.plot_depoleventsgroups_overlayed(possibly_spontfastevents, fast_events,
#                                                    do_baselining=True, do_normalizing=True)
# It's possible that some of the events in there are actually fast-events, but I don't think it's convincing:
# since these events have amp ~1mV the decay shape looks just a bit too noisy to say for sure.




# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
singleneuron_data.plot_depolevents((aps & spont_events),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='spontaneous APs')



















# %% old analysis notes
# notes summary:
# Has fast-events for sure: three groups of amp 7, 8 and 10 mV. Only two examples in the largest two groups,
# but it's enough to make it very clear that the decay is the same.
# I looked for but did not find any events <2mV amp that look like they would have the same rise and decay, too.
#!Note: there's one fast-event happening ~13s into gapFree_withBlockers_0000 - since new file is started
# at the time of solution change, blockers had not actually reached the bath yet.

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'
fast_events = des_df.event_label == 'fastevent'
unlabeled_events = des_df.event_label.isna()
# %%
# analysis summary figures:
# parameter distributions of candidate fast-events and other subthreshold events (=events that are so far still unlabeled)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      fast_events=fast_events,
                                                      other_subthreshold_events=unlabeled_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      fast_events=fast_events,
                                                      other_subthreshold_events=unlabeled_events,
                                                      )
# plot of the fast-events
singleneuron_data.plot_depolevents(fast_events,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='amplitude',  # colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# histograms of parameter distributions
plt.figure()
des_df.loc[fast_events,'amplitude'].plot.hist(bins=30)
plt.title('fast-events amplitudes')

plt.figure()
des_df.loc[:,'rise_time_20_80'].plot.hist(bins=30)
plt.title('all events, rise-time (20-80%amp')

plt.figure()
des_df.loc[fast_events,'rise_time_20_80'].plot.hist(bins=10)
plt.title('fast-events, rise-time (20-80%amp)')

plt.figure()
des_df.loc[:,'width_50'].plot.hist(bins=30)
plt.title('all events, half-width (at50%amp)')

plt.figure()
des_df.loc[fast_events,'width_50'].plot.hist(bins=10)
plt.title('fast-events, half-width (at50%amp)')


# ongoing analysis notes:
# There are clear groups of numerous spikelets with all the same amp (~1mV) and decay (separable coupled neurons?)
# I investigated the smaller events for the possibility that there are fast-events in there, too, by increasingly
# narrowing down parameter windows until it was absolutely clear that the rise/decay shape of small events are
# not at all similar to those of fast-events.
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=(aps | spikeshoulderpeaks))
# %%
singleneuron_data.plot_rawdatablocks('IV', events_to_mark=(aps | spikeshoulderpeaks))
# %%
singleneuron_data.plot_rawdatablocks('shortPulse', events_to_mark=(aps | spikeshoulderpeaks))

singleneuron_data.plot_depolevents(aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms = 200)

# %% quick check: all clearly identifiable events have been labeled
singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=unlabeled_events)
# %%
singleneuron_data.plot_rawdatablocks('IV', events_to_mark=unlabeled_events)
# %%
singleneuron_data.plot_rawdatablocks('shortPulse', events_to_mark=unlabeled_events)
# if there are any events that are obviously noise, label them as such

# my eye picks up some events of 0.5 - 1.5mV amp that could easily just be spikelets/doublets (many of them clearly
# have a two-step rising phase), except that they seem to have disappeared by the time that blockers are applied
# %% parameter distributions of unlabeled events
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_events=unlabeled_events)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_events=unlabeled_events)

# %% looking at parameter distributions of detected subthreshold depolarizations
# (i.e., all events that do not yet have a label)

# the definitely-fast-events have rise-time 0.35-0.6ms and half-width 2.8 - 4.2ms, but since they may be doublets
# I started from a much wider search (rise-time 0.1 - 2 ms, half-width 1.5 - 20ms)
maybestillfastevents_largerthan_params = {'rise_time_20_80':0.3,
                                          'width_50':2.5
                                          }
maybestillfastevents_smallerthan_params = {'rise_time_20_80':1.75,
                                          'width_50':15
                                          }
fastevents_candidates = unlabeled_events
for key, value in maybestillfastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in maybestillfastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_fastevents=fastevents_candidates)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_fastevents=fastevents_candidates)
# up to amp=0.75mV there just seems to be a bunch of events distributed normally,
# with mean rise-time and half-width being ~0.75ms and ~6ms, respectively.
# Above that we may actually be seeing real events:
definitely_events_candidates = (fastevents_candidates & (des_df.amplitude>0.75))
singleneuron_data.plot_depolevents(definitely_events_candidates,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms=50
                                   )

# they're real events alright, but they definitely aren't like the fast-events:
# they all have different peak shape and different decay shape.
singleneuron_data.plot_depoleventsgroups_overlayed(definitely_events_candidates, fast_events,
                                                   group_labels=['small events', 'definitely fast-events'],
                                                   do_baselining=True,
                                                   do_normalizing=True,
                                                   )

# %% labeling of selected events: things that could be fast-events
# first, events that are definitely the thing we think are axonal regenerative events
# fastevents_largerthan_params = {
#                                 'amplitude':2,
#                                 # 'baselinev':-80,
#                                 }
# fastevents_smallerthan_params = {
#                                  'rise_time_20_80': 0.7,
#                                  }
# fastevents_candidates = unlabeled_events
# for key, value in fastevents_largerthan_params.items():
#     fastevents_candidates = fastevents_candidates & (des_df[key] > value)
# for key, value in fastevents_smallerthan_params.items():
#     fastevents_candidates = fastevents_candidates & (des_df[key] < value)
#
# singleneuron_data.plot_depolevents(fastevents_candidates,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    prealignpoint_window_inms=10,
#                                    plotwindow_inms=30,
#                                    plt_title='presumably all fast-events')
# # labeling fast-events as such, and saving the data table
# singleneuron_data.depolarizing_events.event_label[fastevents_candidates] = 'fastevent'
# singleneuron_data.write_results()