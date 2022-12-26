# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220524A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# >1hr recording; not sure about events getting blocked by QX though (mostly because there don't seem to be any at
# the start, but yes in gapFree#2 (~40min after recording started); possibly these are all just (sizeable) spikelets.
# SpikePulse protocol was not carried out properly at varying holding levels.

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# no aps_evokedbylight for this neuron.
# aps_oncurrentpulsechange: all APs for this neuron are evoked by DC, but not all got labeled as such; the ones that did get labeled are all OK.
# aps_spont: indeed, these are all DC-evoked; re-labeling them as such:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents(aps_oncurrentpulsechange,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=50,
                                   prealignpoint_window_inms=20,
                                   do_baselining=False,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
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
# one real event each in gapFree files #0 and 1, and another handful in gapFree #2;
# other than that, all 'events' are DC-evoked, mostly rebound responses that got picked up funny.
# not_spontevents = (unlabeled_spont_events & ~(des_df.file_origin.str.contains('gapFree')))
# not_spontevents2 = (unlabeled_spont_events
#                     & (des_df.file_origin == 'gapFree_0000.abf')
#                     & (des_df.baselinev_idx > (20 * 20000)))
# not_spontevents3 = (unlabeled_spont_events
#                     & (des_df.file_origin == 'gapFree_0001.abf')
#                     & (des_df.baselinev_idx < (100 * 20000)))
# currentpulsechange_events = (not_spontevents | not_spontevents2 | not_spontevents3)
# singleneuron_data.depolarizing_events.loc[currentpulsechange_events, 'event_label'] = 'currentpulsechange_events'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents(unlabeled_spont_events,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )

# I think the remaining 7 events are more likely to be spikelets than fastevents: amplitudes are 2 - 4mV, and risetimes look to be distributed normally around 1.2ms.
