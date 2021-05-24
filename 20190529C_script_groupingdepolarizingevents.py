# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190529C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Very boring neuron really, not surprising given that most of the time it needs a lot of -DC to keep a baselinev.
# Does have fast-events spontaneously, but no APs, and the light-evoked responses are barely perceptible.

# summary plots:
des_df = singleneuron_data.depolarizing_events
fast_events = des_df.event_label == 'fastevent'
fast_events_df = des_df[fast_events]
fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.3 to find good parameter settings; playing with parameters was done elsewhere -
# using saved parameter settings to re-create depolarizing-events data table:
# singleneuron_data.get_depolarizingevents_fromrawdata()


# %% plots: seeing that depolarizing events got extracted nicely

# 1. seeing that evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# I'd say the 'response' to light is mostly just noise if it weren't there really consistently; 1-2mV, slow rise-time.
# This may just be the one IO neuron ever where simply averaging it might make it clearer.

# 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:
# definitely all the fast-events that are easy to pick out by eye (~7-10mV) got picked up, but the great majority
# of events are tiny things with amp < 0.7mV.

# Let's see amplitude and rise-time to narrow down from there:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df))
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
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )

# There are a few points that would indicate relatively large (2-5mV) but also slow (rise-time > 1.5ms) events,
# let's first see what's up with those:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 1.5))
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# Looks to me that there are no fast-events <1.5mV; in the events >1.5mV there's a handful of fast-events (up to ~12mV),
# two oscillation-upslopes, and three or four spikelets that are ALMOST exactly the shape of the fast-events.
# let's find them and mark them as 'noiseevents':
# noiseevents = (possibly_spontfastevents & ((des_df.rise_time_20_80 > 1.5) | (des_df.rise_time_10_90 > 2.5)))
# singleneuron_data.plot_depolevents(noiseevents,
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# not sure what any of those are really supposed to be - osc or spikelet... very noisy either way.
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# I think one of the things we're left with is a spikelet - has a slower decay than the fast-events of the same amp
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# yup, there's one that's 2ms wider than all the rest, all the others should be our fast-events:
# spont_fastevents = (possibly_spontfastevents & (des_df.width_50 < 6))
# singleneuron_data.plot_depolevents(spont_fastevents,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,)
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[spont_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()


# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
# no APs recorded for this neuron
