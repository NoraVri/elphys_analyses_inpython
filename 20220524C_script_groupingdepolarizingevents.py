# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220524C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# a little over 20 minutes recording with ~0.3mMQX; by eye looks like cell has active sodium for the first ~10 minutes.
# Indeed, neuron displays fastevents for the first ~5min. or so, then (DC-evoked) AP shapes start to change
# indicating dependence on Ca-currents instead of Na-ones.

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# no aps_evokedbylight for this neuron.
# aps_oncurrentpulsechange: I saw some APs that should be labeled as current-evoked but didn't (there are no spont.ones);
# otherwise, all these APs got picked up alright (though the baseline-point may not always be great, but this seems to
# also reflect how it gets harder to evoke APs over the course of recordings).
# aps_spont: indeed, all these are actually DC-evoked. Re-labeling as such:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents(aps_oncurrentpulsechange,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=50,
                                   prealignpoint_window_inms=20,
                                   do_baselining=False,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# no TTL-evoked activity for this neuron.


# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# blocknames = des_df[unlabeled_spont_events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=unlabeled_spont_events,
#                                          segments_overlayed=False)
# notes:
# 'events' picked up from files spikePulse 8-10 are in fact currentpulsechanges; re-labeling as such:
# currentpulsechanges = (unlabeled_spont_events
#                        & (des_df.file_origin.str.contains('spikePulse'))
#                        & (des_df.file_origin.str.contains('8|9|10')))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# Events picked up in gapFree_0003 are noise-things occurring where the neuron is hyperpolarized almost down to -100mV.
# labeling them as such:
# noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0003.abf'))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# singleneuron_data.plot_depolevents(unlabeled_spont_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# OK then; aside from the one really slow-rising thing of amp ~2.5mV that occurs spontaneously during the
# last recording file, the 10 other events that got picked up are definitely all fastevents (amps 2.5 - 17.5mV,
# fast rise and identical shape), and the very first event has maxdvdt almost 3x that of all the other events
# (even though some later ones are larger).

# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )

# fastevents = (unlabeled_spont_events & (des_df.rise_time_20_80 < 1))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

