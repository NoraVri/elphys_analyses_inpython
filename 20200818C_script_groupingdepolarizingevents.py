# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200818C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not exactly a great recording: resting baselineV > -40mV on break-in, restores itself a little for about 5 minutes
# but then loses potential again (as well as ability to make APs). Light elicited no response at all.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
aps = des_df.event_label == 'actionpotential'
aps_evokedbyDC = des_df.event_label == 'actionpotential_on_currentpulsechange'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)

# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned()

# %% summary plots - all events:
# the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, aps_evokedbyDC,
                                                   group_labels=['spont', 'DC-evoked'],
                                                   plot_dvdt=True)

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
# no light-evoked APs; spont. and DC-evoked APs got picked up quite nicely.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Light application did not evoke any response in this neuron; not a single event got labeled as evoked.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# not a single event got picked up in this neuron recording.

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# only ~10min. of recording for this neuron, and most of it not very stable in terms of resting baselineV or showing
# any interesting spontaneous activity. So I see no reason to label any neat events for this neuron.