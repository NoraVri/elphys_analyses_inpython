# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221229D'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# patched with QX in the pipette (both intra colors could be seen coming out by the time patch was getting established).
# No spont.fastevents or spont.APs seen; APs can be evoked by electricalStim or DC but look very much driven by Ca.
# Possibly there's a little bit of sodium currents still active in the first ~10min, but definitely not after that.

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


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
# for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbyttl  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: looks alright, even if baselineV point not always great
# aps_evokedbyttl: same as for current-evoked APs
# aps_spont: none to be had really - these all occur within 30ms of depolarizing current onset,
# after baselineV reaches > -30mV. Labeling them as current-evoked:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

# singleneuron_data.plot_depolevents(aps_oncurrentpulsechange, #aps_evokedbyttl,  #aps_spont,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=50,
#                                    prealignpoint_window_inms=20,
#                                    do_baselining=False,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# Seeing that ttl-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# unlabeled_evoked_events = unlabeled_events & evoked_events
# notes:
# saw one event that got picked up as two, and generally baselineV-points are screwed up; but I definitely did not see anything labeled that shouldn't've been.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_spont_events = (spont_events & unlabeled_events)
# notes:
# the only real events are in electricalStim#0, although I strongly suspect these are just spikelets (~2mV amp, slow rise).
# The event picked up in gapFree#1 looks noise-evoked, and in electricalStim#2 there's one noise-thing and one
# ttl-evoked peak that did not get picked up as such because the baselinepoint got put late.
# Labeling these all as noise-events (since we won't do anything with labeled ttl-evoked events anyway, given that automatically extracted measures are unlikely to be good):
# noiseevents = (unlabeled_spont_events & ~(des_df.file_origin == 'electricalStim_0000.abf'))
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
# Indeed, I see no reason why these should be labeled as fastevents (amp < 3mV).

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

# %% looking at activity evoked through electrical stimulation of the pyramidal tract
singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_block=True, prettl_t_inms=-1.5)
# looks to me that electrical stim doesn't evoke any things with fast enough rise-time/high enough max.dVdt to be called fastevents.

# possibly some fast-ish things are getting evoked in the first two stim.files (first 10 minutes of recording)
