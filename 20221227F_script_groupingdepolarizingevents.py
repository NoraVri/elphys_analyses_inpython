# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20221227F'
singleneuron_data = SingleNeuron(neuron_name)
# notes summary:
# QX-intra could be seen coming out of the pipette clearly before patching the neuron;
# some Na-currents may have still been active in the first 5 minutes or so, but probably not anymore after that.


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
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbyttl  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: looks OK; baselineV not always great and APs look like they're mostly Ca-driven, but events that got picked up are definitely all evoked by current and large enough ampplitude to be APs
# Actually, I saw one AP that should be spont.: the very first one to be recorded, it's sitting on a 10pA pulse from seal formation but was definitely not evoked by it.
# Re-labeling it accordingly:
# spont_ap = (aps_oncurrentpulsechange & (des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx < (20000 * 6)))
# singleneuron_data.depolarizing_events.loc[spont_ap, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()

# aps_evokedbyttl: looks like they got picked up as APs mostly because of the huge negative artefact caused by electrical stimulus ('AP' peakV right around 0mV for most of these); definitely all TTL-evoked though
# aps_spont: none of these are really spont., they're evoked by current. Labeling accordingly:
# singleneuron_data.depolarizing_events.loc[aps_spont, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.write_results()
#
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
# looks like all evoked events got picked up; baseline-points are always questionable due to artefact, but peak-points are pretty good

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_spont_events = (spont_events & unlabeled_events)
# notes:
# only three recording files have (some) events that could be real spont. events (gapFree#0 and #1, and shortPulses#2);
# all other 'events' that got picked up are noise-things, small rebound peaks or T-type Ca peaks (neuron likes to make
# big sharkfin oscils, especially when hyperpolarized). Labeling these all as noiseevents (that's what they all are, for our current intents and purposes):
# events_files = ['gapFree_0000.abf', 'gapFree_0001.abf', 'shortPulses_0002.abf']
# noiseevents = ~des_df.file_origin.isin(events_files)
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# The two gapFree files also contain some 'events' that were evoked using the 'one shot'-button on the electrical
# stimulation device; labeling these as ttl-evoked:
# ttlevents_0 = (unlabeled_spont_events
#                & (des_df.file_origin == 'gapFree_0000.abf')
#                & (des_df.peakv_idx < (20000 * 55)))
# ttlevents_1 = (unlabeled_spont_events
#                & (des_df.file_origin == 'gapFree_0001.abf')
#                & (des_df.peakv_idx < (20000 * 250)))
# ttlevents = (ttlevents_0 | ttlevents_1)
# singleneuron_data.depolarizing_events.loc[ttlevents, 'applied_ttlpulse'] = True
# singleneuron_data.write_results()

# events = unlabeled_spont_events  # unlabeled_evoked_events #
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

# We are now left with just 4 events; two of them are definitely proper fastevents (amps 12 and 17 mV, identical
# waveform shape) and the other two look weird. Let's see events parameters:

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

# The event with amp 15mV that doesn't look like a fastevent has a rise-time of just 0.2ms; I'm gonna go with it being a noiseevent. Labeling as such:
# noiseevent = (unlabeled_spont_events & (des_df.rise_time_20_80 < 0.3))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# The other event I think must be counted as a fastevent: with rise-time just over 1ms and amplitude ~4mV it falls just within the criteria.
# Labeling remaining events as fastevents:
# singleneuron_data.depolarizing_events.loc[unlabeled_spont_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% looking at activity evoked through electrical stimulation of the pyramidal tract
singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_block=True, prettl_t_inms=-1.5)
# It sure looks like there's some active response to the electrical stimulation, but it's too slow and broad to be
# fastevent-like; looks more like T-type Ca activation to me.
