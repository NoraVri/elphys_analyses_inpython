# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220524D'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# just under 5 minutes recording, hard to say whether activity is affected by QX.


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# no aps_evokedbylight for this neuron.
# aps_oncurrentpulsechange: about 2 min. after recording start neuron no longer seems to be firing APs at all;
# things labeled as AP are really just big voltage deflections caused by currentpulsechanges.
# Re-labeling events as such:
# currentpulsechanges = (aps_oncurrentpulsechange
#                        & (((des_df.file_origin == 'gapFree_0000.abf')
#                           & (des_df.baselinev_idx > (100 * 20000)))
#                           | (des_df.file_origin == 'spikePulse_0001.abf')))
# Also, the very first two APs look spontaneous to me - they occur while the 50pA tuning pulses are still on,
# but do not seem to be affected by that. Re-labeling them as such:
# spontaps = (aps_oncurrentpulsechange
#             & (des_df.file_origin == 'gapFree_0000.abf')
#             & (des_df.baselinev_idx < (10 * 20000)))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.depolarizing_events.loc[spontaps, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# aps_spont: there's only the two that I just re-labeled (look like they're evoked from fastevent)

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# no TTL-evoked activity for this neuron.


# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# blocknames = des_df[unlabeled_spont_events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=unlabeled_spont_events,
#                                          segments_overlayed=False)
# notes:
# events that got picked up from spikePulse_0001 are all currentpulsechanges;
# the ones in gapFree_0000 are all real events (looks like all are right around 3mV amplitude).
# Re-labeling accordingly:
# currentpulsechanges = (unlabeled_spont_events & (des_df.file_origin == 'spikePulse_0001.abf'))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents(unlabeled_spont_events,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# looks like I missed one wobble occurring at ~-98mV in gapFree_0000; re-labeling it as noiseevent:
# noiseevent = (unlabeled_spont_events & (des_df.baselinev < -90))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# We are left with 9 events with amps 2 - 3.5mV occurring in the first 2.5min. of recordings; I don't think they're
# spikelets though, cause their shape is really very much identical for the most part (one event may be double-wide).
