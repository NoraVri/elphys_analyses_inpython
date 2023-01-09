# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221227E'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# decent enough recording starting out at baselineV ~-50mV, AP peakV almost +50mV;
# according to experiment day notes, cell clearly labeled in QX-color as well by just 15 minutes into recording
# Electrical stimulation device ran out of battery at some point, got replaced

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
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
aps_evokedbyttl = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbyttl  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: debatable whether current pulses continue to elicit APs; but I definitely didn't see anything getting picked up that wasn't on currentpulse.
# aps_evokedbyttl: yup, anything AP-like that's sitting on ttl got picked up now that negative ttl also gets recognized by my algorithm (change to snafs where TTLon is determined)
# aps_spont: just one that got picked up as such, but really it's evoked by the electricalStim (can tell from the artefact that precedes it, and the fact that I was clearly playing with the 'one shot' button in this stretch of recording).
# Re-labeling it as such:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'applied_ttlpulse'] = True
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
des_df = singleneuron_data.depolarizing_events
nbins = 100
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# Seeing that ttl-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
unlabeled_evoked_events = unlabeled_events & evoked_events
# notes:
# baseline-points are not to be trusted (as expected with electrical stim artefact) and there may be a few events that didn't get labeled as ttl-evoked but should have; did not see any events labeled that shouldn't've been.

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_spont_events = (spont_events & unlabeled_events)
# notes:
# 25 events got picked up, but only one that's a proper spontaneous fastevent; most others are evoked by electricalStim
# via the 'single shot'-button on the stimulator, and the one spontaneous event picked up in electricalStim#1 looks like
# a Ca-spike (may have been set off by a fastevent).
# Labeling the fastevent:
# fastevent = (unlabeled_spont_events
#              & (des_df.file_origin == 'gapFree_0000.abf')
#              & (des_df.baselinev_idx > (180 * 20000)))
# singleneuron_data.depolarizing_events.loc[fastevent, 'event_label'] = 'fastevent'
# Labeling the stim-triggered events as evoked:
# ttlevoked_events = (unlabeled_spont_events
#                     & (des_df.file_origin == 'gapFree_0000.abf')
#                     & ~fastevent)
# singleneuron_data.depolarizing_events.loc[ttlevoked_events, 'applied_ttlpulse'] = True
# singleneuron_data.write_results()

# events = unlabeled_spont_events
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####




