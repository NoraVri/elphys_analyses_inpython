# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220525G'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# nothing much of spontaneous activity, and seems to mostly retain its ability to fire Na-APs over the course of 25min. recording.


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
# aps_oncurrentpulsechange: all APs that got picked up as such are indeed evoked by current (as are all APs in this neuron).
# aps_spont: these are all also DC-evoked - seems it takes quite a lot of slow, steady depolarization to get to the AP threshold.
# re-labeling them as such:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

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
# they're basically all either degenerate spikes or rebound events occurring in response to current changes
# (one ~2mV amp wavelet picked up in gapFree_0001 may be something else, but it happens on top of a currentpulse at
# V ~-10mV so who knows what it is exactly - leaving it unlabeled).
# re-labeling other events:
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'events_on_currentpulsechange'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
