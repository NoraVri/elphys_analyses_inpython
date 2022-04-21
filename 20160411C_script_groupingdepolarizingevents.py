# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20160411C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# This neuron is from before the datacollection used for the morphologies paper; in the latest picture Yoe took of it
# it's very clear what's the axon and that it has at least one big complex spine there.
# Unfortunately, it doesn't seem to have any spontaneously occurring fastevents (or APs, for that matter)

# summary plots:
des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
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
singleneuron_data.plot_depolevents(aps, colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
# singleneuron_data.write_results()



# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:


# Let's see some events, and their amplitude and rise-time to narrow down from there:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 1.5))
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   newplot_per_event=True, display_measures=True
                                   )
# %%
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
