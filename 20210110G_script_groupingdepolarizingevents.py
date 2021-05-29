# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210110G'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# very boring neuron, barely doing anything at all, let alone making fast-events or responses to light
# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=10, min_depolamp=2)
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# only 7 events detected altogether, 4 of those are noise.

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
