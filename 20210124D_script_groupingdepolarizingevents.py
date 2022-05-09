# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124D'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not the greatest recording: cell clearly gets leaky after ~4minutes (before any light applied), and doesn't do much
# of anything spontaneously besides oscillating (osc amp decreasing from ~15 to 1mV over the first 5 minutes).
# Light response usually seems to include fast things, occasionally AP.

# %% plotting light-evoked activity:
singleneuron_data.plot_rawdatatraces_ttlaligned()


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
# APs all got picked up nicely (two light-evoked, one spont., the rest DC-evoked), except three got labeled spont.
# even though they are clearly evoked by the +DC current pulse they are sitting on. Re-labeling these:
# aps_oncurrent = (aps_spont & (des_df.peakv_idx < (20000 * 300)))
# singleneuron_data.depolarizing_events.loc[aps_oncurrent, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# light-evoked responses of >2mV amp all picked up nicely; did not see anyting labeled that should in fact be spont.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# no real events got picked up, just noise-things. Labeling as such:
# singleneuron_data.depolarizing_events.loc[unlabeled_events, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# neuron has about 8min. of nice recording but no spont.events there whatsoever; so I see no reason to mark neatevents for this neuron.