# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200708C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not too stable recording of a neuron doing nothing spontaneously except keep a wobbly baselineV and one AP;
# light barely evokes a small (3mV) slow response except once it evokes an AP.

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse

# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()

# %% summary plots - all events:
singleneuron_data.plot_depoleventsgroups_overlayed((aps & spont_events), (aps & ~spont_events),
                                                   group_labels=['spont', 'light-evoked'],
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
# the two APs (light-evoked and spont) got picked up properly (no DC pulses to see spikes).
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# very few evoked things actually got picked up, because amp so small. Definitely
# nothing that is in fact spontaneous got picked up as evoked.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# not a single spontaneous event picked up for this neuron. Indeed I did not see any rise above the noise in the raw data.

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# Not marking neatevents for this neuron: AP peakV only +10mV to start with and baselineV quite noisy, so looks to me
# that this not a neat enough recording to be included in that pile.

