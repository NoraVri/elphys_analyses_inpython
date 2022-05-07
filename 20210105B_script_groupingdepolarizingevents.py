# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210105B'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not the greatest recording: neuron not quite oscillating most of the time, just showing noisy baselineV;
# light response looks rather nice though, clear synaptic response with fast things often riding on top and the
# occasional evoked AP (at the most depolarized baselineV).

# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned()


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
# no DC-evoked APs in this neuron (DC pulses to see spikes not applied)
# light-evoked APs got picked up nicely (including baselinepoints), as did the single spont.AP
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# looks like evoked events of >2mV amp all got picked up, though neither baseline- nor peak-points
# are always all that great. Did not see anything labeled that should in fact be spont.

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# Exactly two 'spontaneous events' got picked up: one occurs during the final recording file where neuron suddenly
# depolarizes a bunch, the other is a proper fastevent (10mV amp). Labeling it:
singleneuron_data.depolarizing_events.loc[(unlabeled_spont_events & (des_df.file_origin == 'light_0002.abf'),
                                           'event_label')] = 'fastevent'
singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# not including this neuron's data in neat-events: baselineV too noisy and variable, and anyway there's exactly 1 AP and 1 fastevent spontaneously.