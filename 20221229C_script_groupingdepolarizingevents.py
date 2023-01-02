# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221229C'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# neuron patched with QX-free intra in the tip of the pipette, which was otherwise filled with QX-containing intra (~1mM).
# didn't get labeled in QX-color for at least 15 minutes after getting patched, according to notes;
# by about half an hour into recording it was getting QX-colored, at least in the soma.
# TTL trigger marks electrical stimulus to pyramidal tract.

# No spont. APs in this neuron (except where riding depolarizing current taking V > -25mV).
# Spontaneous fastevents are highly infrequent from the start, and the last ones occur ~20min. after patch established.


# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
aps_evokedbyttl = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
spont_events = ~des_df.applied_ttlpulse  #


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
# # # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbyttl  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: all events that got picked up as such are indeed on a currentpulse; debatable whether they
# are all APs (lots of things evoked with short, large current pulses that always cause large voltage deflection which
# occasionally gets picked up as AP even if nothing active is actually evoked).
# aps_evokedbyttl: not everything that I would classify as AP indeed got labeled as such automatically, and those that
# did get picked up as APs mostly got weird baseline-points because of the stimulus artefact.
# Did not see anything picked up as ttl-evoked that should not have been.
# aps_spont: this neuron doesn't fire any APs spontaneously really, except for where current pulses take the baseline
# voltage to ~-20mV or higher, which happens here on depolarizing current pulses.
# singleneuron_data.plot_depolevents(aps_oncurrentpulsechange, #aps_evokedbyttl,  #aps_spont,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=50,
#                                    prealignpoint_window_inms=20,
#                                    do_baselining=False,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# Seeing that ttl-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# unlabeled_evoked_events = unlabeled_events & evoked_events
# notes:
# probably not everything that could've gotten picked up did; but I did not see anything labeled as 'evoked' that shouldn't've been.


# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_spont_events = (spont_events & unlabeled_events)
# notes:
# there's just a handful of actual spontaneous fastevents, mostly in gapFree files and one in electricalStim#0.
# The 'events' in electricalStim#2 are all noise-things, labeling them as such:
# noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'electricalStim_0002.abf'))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# In electricalStim#4, 5, and 6 there's only currentpulsechanges that didn't get labeled as such; doing it now:
# currentpulsechange_events = (unlabeled_spont_events
#                              & (des_df.file_origin.str.contains('Stim'))
#                              & ~(des_df.file_origin.str.contains('_0000.abf')))
# singleneuron_data.depolarizing_events.loc[currentpulsechange_events, 'event_label'] = 'currentpulsechange'
# Finally, the first two 'events' occurring in gapFree#2 are noise-things as well; labeling them as such:
# noiseevents = (unlabeled_spont_events & (des_df.file_origin == 'gapFree_0002.abf') & (des_df.baselinev_idx < (100 * 20000)))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# events = unlabeled_evoked_events # unlabeled_spont_events
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)

# singleneuron_data.plot_depolevents(unlabeled_spont_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
#
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# I see no reason why all remaining events shouldn't be fastevents: amplitudes are 4-10mV, rise-times all <1.2ms and
# if the event shapes aren't all exactly identical, it's probably because the last there occurred after the cell crashed
# a little and then regained itself. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

# %% looking at activity evoked through electrical stimulation of the pyramidal tract
singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_block=True, prettl_t_inms=-2)
# looks to me that electrical stim doesn't evoke any things with fast enough rise-time/high enough max.dVdt to be called fastevents.

