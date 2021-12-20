# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210426D'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# has some nice fast-events, but also clearly deteriorating APs (their amp goes gradually down, and pretty soon they barely reach 0mV at their peak)

# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True, postttl_t_inms=20)
# separately by conditions: low/high light intensity, small/large light spot
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000',
                                                plt_title='low light intensity, large field')
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0001', 'light_0002',
                                                newplot_per_ttlduration=True,
                                                plt_title='high light intensity, large field')
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0003',
                                                plt_title='high light intensity, small field')
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# Using default parameter settings for extracting depolarizing events; for starters getting only events >2mV.
# Looking at the raw data with picked-up events marked - there's a few light-responses that rise rather slowly,
# got a bad baseline-point (peaks are OK though) and got marked spontaneous. Extending ttleffect_window to get these
# labeled correctly:
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=7)
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

# Let's filter down, and see amplitude and rise-time to narrow down from there:
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


# singlevoltage_possiblyfastevents = (possibly_spontfastevents & (des_df.baselinev > -50) & (des_df.baselinev < -45))
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )



# Let's check that there isn't things in the previously filtered events that are very clearly fast-events, too;

