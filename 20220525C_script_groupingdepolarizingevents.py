# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220525C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# nothing much of spontaneous activity (occasionally ~3mV events that could easily be spikelets), and
# seems to mostly retain its ability to fire Na-APs over the course of 25min. recording.

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
# aps_oncurrentpulsechange: not all APs got picked up as such, even though all APs this neuron has are DC-evoked
# aps_spont: indeed, all the rest of APs are here. Re-labeling them as aps_on_currentpulsechange:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

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
blocknames = des_df[unlabeled_spont_events].file_origin.unique()
if len(blocknames) > 0:
    singleneuron_data.plot_rawdatablocks(*blocknames,
                                         events_to_mark=unlabeled_spont_events,
                                         segments_overlayed=False)
# notes:
# three 'events' are currentpulsechanges that got picked up weird (one in gapFree_0001, one in spikePulse_0001, and the one event in spikePulse_0002)
# bunch of rebound responses in spikePulse_0001 that got picked up as events;
# and two peaks that occur on currentpulsechanges in gapFree_0001 will all need to be filtered out;
# the rest are few and still all just look like spikelets to me.
# currentpulsechange_events_gf1 = (unlabeled_spont_events
#                              & (des_df.file_origin == 'gapFree_0001.abf')
#                              & ((des_df.baselinev_idx < (170 * 20000))
#                                 | ((des_df.baselinev_idx > (900 * 20000)) & (des_df.baselinev_idx < (960 * 20000)))))
# currentpulsechange_events_sp1 = (unlabeled_spont_events
#                                  & (des_df.file_origin == 'spikePulse_0001.abf')
#                                  & (des_df.segment_idx == 1)
#                                  & (des_df.amplitude < 1))
# currentpulsechange_events_sp2 = (unlabeled_spont_events & (des_df.file_origin == 'spikePulse_0002.abf'))
# currentpulsechange_events = (currentpulsechange_events_gf1 | currentpulsechange_events_sp2 | currentpulsechange_events_sp1)
# singleneuron_data.depolarizing_events.loc[currentpulsechange_events, 'event_label'] = 'currentpulsechange_events'
# singleneuron_data.write_results()
# In the now remaining events, those in spikePulse_0001 are all rebound responses; labeling them as such:
# rebound_events = (unlabeled_spont_events & (des_df.file_origin == 'spikePulse_0001.abf'))
# singleneuron_data.depolarizing_events.loc[rebound_events, 'event_label'] = 'rebound_events'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents(unlabeled_spont_events,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

# Of the now remaining handful of events, the largest has amp 3.75mV, but it'd be
# impossible to say which might be fast enough to be fastevents and not spikelets.
