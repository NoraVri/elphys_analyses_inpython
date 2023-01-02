# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221229E'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# neuron patched with delayed-QX effect (at least 10 min. where cell is not labeled in QX-color, and keeps doing fastevents).
# has fastevents occurring in the first ~15 min. or so of recording, and none in the last ~15 min. or so.

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
aps_evokedbyttl = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
spont_events = ~des_df.applied_ttlpulse  #


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2 and ttleffect_window=15

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=15)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbyttl = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbyttl  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: looks like there may be more that should be categorized as such, but definitely I didn't see anything picked up that shouldn't've been.
# aps_evokedbyttl: got picked up alright in general, although stimulus artefact causes bad baslineV points which got a few responses labeled as AP even though they are really subthreshold (but I don't really care, probably won't use this labeling anyway).
# aps_spont: two occurring at resting baselineV, three at V>-25mV but more than 30ms after depolarizing current onset.

# singleneuron_data.plot_depolevents(aps_oncurrentpulsechange, #aps_evokedbyttl,  #aps_spont,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=50,
#                                    prealignpoint_window_inms=20,
#                                    do_baselining=False,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# singleneuron_data.plot_depolevents(aps_spont,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=6,
#                                    prealignpoint_window_inms=3,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plot_ddvdt=True
#                                    )
# The two APs occurring at resting baselineV are definitely evoked from fastevents.

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# Seeing that ttl-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# unlabeled_evoked_events = unlabeled_events & evoked_events
# notes:
# looks like they generally got picked up, though baseline-points often bad as usual with electricalStim-evoked stuff.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_spont_events = (spont_events & unlabeled_events)
# notes:
# All real spont.events, except for some in gapFree_0000: five noise-things that are riding strongly
# depolarizing current pulses and one other noise-evoked thing are gonna need to be re-labeled.
# noiseevents = (unlabeled_spont_events
#                & ((des_df.baselinev > -25) | (des_df.amplitude > 15)))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# events = unlabeled_evoked_events # unlabeled_spont_events
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)

# singleneuron_data.plot_depolevents(unlabeled_spont_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# There's no way these aren't all fastevents. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

# %% looking at activity evoked through electrical stimulation of the pyramidal tract
singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_block=True, prettl_t_inms=-1.5)




