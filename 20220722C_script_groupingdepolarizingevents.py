# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220722C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# 2hr-long recording of neuron doing lots of things spontaneously, including fast-events so big I mistook them for
# APs at first (peakV > 0). Also, successful TTX application and washout (at least as far as APs).

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
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# no aps_evokedbylight for this neuron.
# aps_oncurrentpulsechange: most DC-evoked APs indeed got labeled as such by the algorithm; even APs labeled as evoked
# in shortPulses files are mostly that - the ~4mV depolarization is enough to evoke APs at resting baselineV roughly 2/3 times.
# aps_spont: interestingly, this neuron fires APs with a frequency on depolarization - those APs are mostly labeled
# spont (they occur from way depolarized baselineV but otherwise not directly evoked by change in current).
# A few APs need re-labeling:
# 2 APs occurring within 25ms of +DC pulse in gapFree_0000:
# aps_oncurrentpulsechange_gf0 = (aps_spont
#                                 & (des_df.file_origin == 'gapFree_0000.abf')
#                                 & (des_df.baselinev_idx < (75 * 20000)))
# # 2 more in gapFree_0003:
# aps_oncurrentpulsechange_gf3 = (aps_spont
#                                 & (des_df.file_origin == 'gapFree_0003.abf')
#                                 & (des_df.baselinev_idx > (63 * 20000))
#                                 & (des_df.baselinev_idx < (68 * 20000)))
# # and one in gapFree_withTTXx3_0000 (the only one there):
# aps_oncurrentpulsechange_gfTTXx3 = (aps_spont & (des_df.file_origin == 'gapFree_withTTXx3_0000.abf'))
# # finally, one AP occurring in response to release from mild hyperpolarizing DC in shortPulses_0002:
# aps_oncurrentpulsechange_sp2 = (aps_spont
#                                 & (des_df.file_origin == 'shortPulses_0002.abf')
#                                 & (des_df.segment_idx == 53))
# aps_on_currentpulsechange = (aps_oncurrentpulsechange_gf0
#                              | aps_oncurrentpulsechange_gf3
#                              | aps_oncurrentpulsechange_gfTTXx3
#                              | aps_oncurrentpulsechange_sp2)
# singleneuron_data.depolarizing_events.loc[aps_on_currentpulsechange, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()

singleneuron_data.plot_depolevents((aps_spont
                                    & (des_df.baselinev < -50)
                                    & (des_df.maxdvdt > 7)
                                    ),
                                   colorby_measure='baselinev',
                                   plotwindow_inms=50,
                                   prealignpoint_window_inms=20,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   # plot_ddvdt=True
                                   )
# interesting. There are some APs that are definitely APs (peakV way up there with all the others) but have a very
# barely perceptible, practically non-existent shoulder (while APs occurring at just a bit more depolarized potential
# tend to have really broad shoulders).

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
# events mostly got picked up very nicely; wherever they didn't it's mostly the data being weird and/or bad.
# In gapFree_withTTXx3washout_0001, in the last minute or so of recording (where neuron is no longer held with -DC)
# the neuron is way far depolarized (~-35mV) relative to its original resting baseline voltage (~-60mV) and doing all
# sorts of weird noisy things, firing APs that barely reach over 0mV peakV. Labeling all events occurring in this
# stretch of recording as 'noiseevents':
# noiseevents = (des_df.file_origin == 'gapFree_withTTXx3washout_0001.abf') & (des_df.baselinev_idx > (951 * 20000))
# # Next up, all 'events' in longPulses_0000 are weird things happening on top of depolarizing current pulses;
# # labeling these as 'noiseevents' as well:
# noiseevents2 = (unlabeled_spont_events & (des_df.file_origin == 'longPulses_0000.abf'))
# # and one 'event' in shortPulses_0003 is a woblle on a spikeshoulder (AP got cut by end of sweep), labeling it as noise, too:
# noisevent = (unlabeled_spont_events & (des_df.file_origin == 'shortPulses_0003.abf'))
# noiseevents_all = (noisevent | noiseevents2 | noiseevents)
# singleneuron_data.depolarizing_events.loc[noiseevents_all, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# Having seen the remaining events there's one left that's some kind of noise-wobble occurring on a depolarizing current pulse. Labeling it as noise:
# noiseevent = (unlabeled_spont_events & (des_df.baselinev > -30))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

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
# the remaining unlabeled subthreshold events have to be all fastevents: fast rise-times, amplitude groups (5 and 10mV)
# and identical waveforms. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####

