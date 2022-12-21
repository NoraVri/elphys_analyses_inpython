# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220531C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# nice recording of an IO cell patched with a pipette containing QX-free intra in the tip,
# and further back-filled with intra containing QX

des_df = singleneuron_data.depolarizing_events





# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# extracting with default parameters for finding large depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_spont  #aps_oncurrentpulsechange  #aps_evokedbylight
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# 'aps' occurring during the first ~40s of the trace are just noiseevents occurring on currentpulsechanges;
# labeling them as such:
# noiseevents_on_currentpulses = (aps_oncurrentpulsechange
#                                 & (des_df.file_origin == 'gapFree_0001.abf')
#                                 & (des_df.baselinev_idx < (40 * 20000)))
# singleneuron_data.depolarizing_events.loc[noiseevents_on_currentpulses, 'event_label'] = 'noiseevent_on_currentpulsechange'
# Other than that, not all APs that are on a currentpulsechange got marked as such, but
# all APs that got marked as 'on_currentpulsechange' are indeed on a currentpulsechange (though sometimes just before).
# Marking APs that got labeled 'spont' but are in fact on currentpulsechange (cell is slow to respond with APs,
# possibly because they are dendritic Ca-spikes evoked in the presence of QX)
# aps_on_currentpulsechange = (aps_spont & (des_df.file_origin.str.contains('longPulses')))
# singleneuron_data.depolarizing_events.loc[aps_on_currentpulsechange, 'event_label'] = 'actionpotential_on_currentpulsechange'
# and the last AP in file gapFree_0001 is also on a currentpulsechange; labeling as such:
# ap_on_currentpulsechange = (aps_spont & (des_df.file_origin == 'gapFree_0001.abf')
#                             & (des_df.baselinev_idx > (700 * 20000)))
# singleneuron_data.depolarizing_events.loc[ap_on_currentpulsechange, 'event_label'] = 'actionpotential_on_currentpulsechange'

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# no ttl-evoked events in this neuron.

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
# spontaneous events all got picked up nicely; in file gapFree_0001 there are some noiseevents (a group early on,
# riding large de/hyperpolarizing current pulses; and one more later on probably from touching the rig).
# Labeling these as such:
# noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0001.abf')
#                & ((des_df.baselinev_idx < (140 * 20000)) | (des_df.baselinev_idx > (600 * 20000))))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting all as-yet unlabeled events parameters:
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

singleneuron_data.plot_depolevents(unlabeled_spont_events,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )

# Labeling fast-events and other events fitting in categories not labeled automatically (fastevent, compound_event, other_event, noiseevent)
# By amplitude, rise-time and half-width parameters and gradually changing normalized shape, it looks to me that all the remaining subthreshold events should be counted as fastevents.



# %% seeing all APs
spikepulse_aps = (aps_oncurrentpulsechange & (des_df.file_origin.str.contains('spike')))
otherpulse_aps = (aps_oncurrentpulsechange & ~(des_df.file_origin.str.contains('spike')))
singleneuron_data.plot_depolevents(spikepulse_aps,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   plt_title='spike pulse APs'
                                   )
singleneuron_data.plot_depolevents(otherpulse_aps,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   plt_title='other DC-evoked APs'
                                   )

singleneuron_data.plot_depolevents(aps_spont,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   plt_title='spont APs'
                                   )


