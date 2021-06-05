# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np


neuron_name = '20190529B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# This neuron does not have any spontaneous fast-events of any kind (only tons of tiny spikelets);
# not surprising considering that it's not all that healthy (held with quite a lot of -DC most of the time).
# Its evoked events are worth taking a closer look at though: at first look they behave rather like fast-events would.
# Evoked APs especially are a mess of all sorts of depolarizations happening...
# summary plots:
des_df = singleneuron_data.depolarizing_events
evoked_events = des_df.applied_ttlpulse
spont_events = ~evoked_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)

nbins = 60
plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=nbins) # 60bins to start with
plt.title('spont. events, amplitude')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=nbins)
plt.title('spont. events, rise-time (20-80%)')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=nbins)
plt.title('spont. events, rise-time (10-90%)')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )

singleneuron_data.plot_depolevents((aps & des_df.applied_ttlpulse),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms = 50,
                                   plt_title='light-evoked APs')
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.2  to find good parameter settings; playing with parameters was done elsewhere somewhere;
# using saved parameter settings to re-create depolarizing-events data table:
# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=12)


# 1. seeing that evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# The algorithm quite regularly picks up a second baseline/peak pair in the light-evoked response; that
# looks right to me though even in cases where the light stimulus is very short (add ChR activation time constant and it's well within range).
# Noticed later that in many cases, this second peak is marked not marked as TTL-evoked, so ran the algorithm again.

# 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# Loads of stuff got picked up, nothing really that looks like fast-events though... Let's start narrowing it down:
# There's exactly one sweep during which the neuron oscillates (and doesn't do anything else)
# and osc.upslopes are picked up as 'events'. Labeling all these as noise-events:
# oscupslope_events = des_df.file_origin == 'light_0000.abf'
# singleneuron_data.depolarizing_events.loc[oscupslope_events, 'event_label'] = 'noiseevent'
# And in gapFree_0000, there's a weird noise-thing that got picked up as three events (that are rather big;
# they are the only three events between 351 - 351.05 s in the trace [but account also for the 18s cut off trace start])
# Labeling these as noise-events, too:
# sampling_rate = float(singleneuron_data.blocks[0].segments[0].analogsignals[0].sampling_rate)  # in Hz
# noise_startidx = (351 - 18) * sampling_rate
# noise_endidx = (351.05 - 18) * sampling_rate
# noiseevents_byeye = ((des_df.file_origin == 'gapFree_0000.abf')
#                      & (des_df.peakv_idx > noise_startidx) & (des_df.peakv_idx < noise_endidx))
# singleneuron_data.depolarizing_events.loc[noiseevents_byeye, 'event_label'] = 'noiseevent'


# Let's see what we're left with:
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
# the rise-time histograms would appear to have some grouping, not the amplitude one - there is nothing
# that would look like a fast-event by parameters. All events except 1 are <1.5mV.


# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
# singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
# singleneuron_data.plot_depolevents((aps & ~des_df.applied_ttlpulse),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
#
# singleneuron_data.plot_depolevents((aps & des_df.applied_ttlpulse),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='light-evoked APs')
# interestingly, the majority of light-evoked APs has no shoulder - looks more like a fast-event or AIS spike.
# (identical normalized decay except for decay slowing down for more depolarized baselinev; and then there's this
# one group of events that for some reason has a particularly fast decay).
# Also, almost all these APs seem to be evoked by rather high amplitude, wide pre-potentials, and the baseline-points
# are not always so well found by the algorithm.



