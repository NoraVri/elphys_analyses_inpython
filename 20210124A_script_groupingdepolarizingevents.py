# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:


# summary plots:
des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
fast_events = des_df.event_label == 'fastevent'
# compound_events = des_df.event_label == 'compound_event'

# fast_events_df = des_df[fast_events]
# fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
# singleneuron_data.plot_depolevents(fast_events,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    )
# singleneuron_data.plot_depolevents(fast_events,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)

singleneuron_data.plot_depolevents(aps,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True
                                   )

# singleneuron_data.plot_depolevents(compound_events,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events; for starters getting only events >2mV.
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# looks good; there really isn't much of a response to the light at all besides the occasional spikelet and perhaps
# changes in the oscillations (then again this neuron is doing all sorts of stuff all over the place so who knows).

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# This neuron has TONS of fast-events (amp up to almost 20mV), and it's very clear that more APs occur at more
# depolarized baselinev. Baselinev is manipulated by DC injection for nice periods of time, but there is also a general
# drift of baselinev downwards (-50mV w/o DC in the beginning, -60mV at the end of recordings).
# My eye also picked up some events that are doubles, or look more round - this seems to be the case especially for the
# largest of events, and possibly only where baselinev is hyperpolarized (AIS spike that doesn't reach full AP?).

# Let's see some events and their parameters and take it from there:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df))
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
nbins = 50
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
# by the scatters there's gonna be some outliers to clean out of there - indeed, some noisy things are visible in the
# plotted traces. Other than that, it's clear that this neuron has at least 4 or 5 amplitude-groups of events,
# irregularly spaced between 5 and 17.5mV and with the largest events being least frequent.

# Let's see