# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190529E'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# pretty boring neuron, doing nothing spontaneously except maintaining baselineV (-50 - -60mV) until it gets suddenly
# more leaky during the third light-applied block; soon after that it also stops responding to light altogether
# (before that we consistently get 2 - 4mV response to light).

# no fastevents, no neat events. Some APs evoked by DC.

# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned()
# note: consistent response to light only in the first three blocks (light 0 - 2); barely a response in light#3, and
# after that no response at all.
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
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# no light-evoked or spont.aps in this neuron; ones on currentpulse all got labeled right automatically.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# light-evoked responses all got picked up very nicely (with good baseline-points, too), except where amp < 2mV.


# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# just 2 spont.events picked up in the whole entire recording (of almost 1/2hr), and neither of them are proper:
# the first is definitely some sort of depolarizing event, but amp (just over 3mV) and rise-time (~1.5ms) measurements
# make me think it's more likely to be a spikelet than a fastevent. The other 'event' is a place where the neuron
# suddenly depolarizes by ~5mV over a period of 10ms, and does not return to its previous baselinev. So, I'm
# not labeling any fastevents for this neuron.

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# I don't think there's a point to marking any part of this recording as 'neat', given that there are no events in there.
