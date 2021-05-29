# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200630C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# summary plots:
# des_df = singleneuron_data.depolarizing_events
# aps = des_df.event_label == 'actionpotential'
# fast_events = des_df.event_label == 'fastevent'
# fast_events_df = des_df[fast_events]
# fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
# singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)
# singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=10)
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# looks pretty good - definitely all evoked events got labeled as such; quite often the baselinepoint isn't where
# we would put it by eye because evoked events are rather compound.


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# There's a couple of noisy things that got picked up as events, but other than that it looks good;
# the cell is mostly pretty quiet with the occasional small spikelet (amp ~1mV) and fast-events starting at 4mV amp.

# Let's see some events, and their amplitude and rise-time to narrow down from there:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df))
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   )
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
nbins = 20
possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_70',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# It's very clear from these plots which ones are the two noiseevents: they have much longer rise and width than all the others.
# Labeling them as such:
# noiseevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 2))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# Let's see the remaining events:
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   timealignto_measure='rt20_start_idx',
                                   prealignpoint_window_inms=1,
                                   plotwindow_inms=10,
                                   plot_dvdt=True,
                                   )
