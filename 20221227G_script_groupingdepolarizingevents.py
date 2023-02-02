# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221227G'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# Neuron patched with QX-free intra in the tip; soma was faintly labeled by the time pipette was removed from the slice,
# however the neuron died already well before then.
# Looks like neuron is able to do Na-spikes throughout recording.


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

# aps_oncurrentpulsechange: looks all OK
# aps_evokedbyttl: not sure I'd call these APs, but peakV for detected events goes just over 0mV so I guess it fits well enough.
# aps_spont: one got labeled as such, however it's definitely evoked by current (occurring within 30ms from depol.current step).
# Re-labeling it accordingly:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# Seeing that ttl-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# unlabeled_evoked_events = unlabeled_events & evoked_events
# notes:
# Looks OK

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_spont_events = (spont_events & unlabeled_events)
# notes:
# just a single event in the entire recording, and a few noise-things riding a depolarizing current pulse;
# the single event has weirdly fast rise-time and amp only ~4mV, so I am loath to mark it as fastevent all by itself.
# Leaving everything unlabeled.

# events = unlabeled_evoked_events # unlabeled_spont_events
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

