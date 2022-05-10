# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210426B'
singleneuron_data = SingleNeuron(neuron_name)

singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# not the greatest recording: resting baselineV just below -30mV, and neuron dies altogether
# after just 7 light pulses - but 6 of those evoke an AP and one a fastevent.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label

# %% plotting light-evoked activity
singleneuron_data.plot_rawdatatraces_ttlaligned()


# %% summary plots - all events:
# the main events-groups, overlayed (aps, fastevents)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, fastevents,
                                                   group_labels=['aps', 'fastevents'],
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
# the first ap_oncurrentpulse is in fact spont, it occurs just before application of a -DC pulse
# singleneuron_data.depolarizing_events.loc[(aps_oncurrentpulsechange & (des_df.peakv_idx < (20000*25))),
#                                           'event_label'] = 'actionpotential'
# and the aps_spont group contains two that are in fact very much evoked by the +DC pulse they're riding:
# singleneuron_data.depolarizing_events.loc[(aps_spont
#                                            & (des_df.peakv_idx > (20000*111)) & (des_df.peakv_idx < (20000*126))),
#                                           'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# light-evoked events all got picked up nicely; nothing that isn't evoked got labeled

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# all things that look like real events got picked up, as well as two noise-things riding the bottom
# of hyperpolarizing current pulses. Labeling as such:
# noiseevents = (unlabeled_spont_events & (des_df.baselinev < -70))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# plotting all as-yet unlabeled events parameters:
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       unlabeled_spont_events=unlabeled_spont_events,
#                                                       )
#
# singleneuron_data.plot_depolevents(unlabeled_spont_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# I see no reason why these wouldn't all be fastevents: amps 5 - 8mV, rise-time < 1.2ms for all.
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# noisy recording with very unsteady baselineV and AP amp; I see no reason to include it in neat-events.