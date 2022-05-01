# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210411F'
singleneuron_data = SingleNeuron(neuron_name)
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# neuron has bad baselineV throughout (~-30mV if at all, with -2nA DC) but is happily oscillating
# and doing fastevents nonetheless, also in response to light.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
compound_events = des_df.event_label == 'compound_event'
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise
# %% plotting light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_ttlduration=True)

# separately by conditions: small/large illumination field size, and intensity
# small spot low intensity: files 2, 4, 6
singleneuron_data.plot_rawdatatraces_ttlaligned('2', '4', '6',
                                                plt_title='small field, low intensity',
                                                postttl_t_inms=20)
# large spot low intensity: files 1, 3, 7
singleneuron_data.plot_rawdatatraces_ttlaligned('1', '3', '7',
                                                plt_title='large field, low intensity',
                                                postttl_t_inms=20)
# large spot high intensity: files 0, 5, 8
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000', '5', '8',
                                                plt_title='large field, high intensity',
                                                postttl_t_inms=20)

# %% summary plots - all events:
# histogram of baselinev in the entire recording:
# singleneuron_data.get_timespentrecording(make_baselinev_hist=True)
# histograms of events parameters
nbins = 100
# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('fast-events parameter distributions')

# compound events
des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('compound events parameter distributions')

# spikelets
des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('smallslowevents parameter distributions')

# action potentials
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('aps parameter distributions')

# line plots:
# the main events-groups, overlayed (aps, fastevents, compound events)
singleneuron_data.plot_depoleventsgroups_overlayed(aps, compound_events, fastevents,
                                                   group_labels=['aps', 'compound_events', 'fastevents'],
                                                   )
# fast-events:
singleneuron_data.plot_depolevents(fastevents,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# exttracting with standard parameters, min_depolamp 1mV (from seeing the raw data there's a spikelet of ~1mV, and nothing smaller)
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1)
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
# nothing got labeled as AP automatically, and indeed I did not see anything with peakV >0mV in the raw data.
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# not all evoked responses got picked up as events - some are small and slow and didn't make it with the extraction
# parameter settings used. Of those that did get picked up, the baselineV point isn't always great, but that's mostly
# because the evoked response is rather compound.

# Seeing that spontaneous fast-events got picked up:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# looks quite good. At first sight it seemed that there are quite a few events that didn't get picked up in the first
# recording file, but closer inspection says that those are all spikelets with amp ~1mV; the smallest fastevent that
# I saw has amp ~2.5mV. And even though the recording is quite noisy at times, not a lot of noise got picked up: I saw
# just 4 'events' that aren't actually events.

# Finding and labeling fast-events (and other types of events encountered along the way):
# Let's start by labeling the noiseevents as such, from their location within the raw data:
# noiseevents = (des_df.file_origin == 'light_0009.abf') & (des_df.segment_idx == 7)
# noiseevents = noiseevents | ((des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx > 1800000))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# Now let's see parameter distributions to decide what are fastevents:
# plotting all as-yet unlabeled events parameters:
# nbins = 100
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
# %%
# From the parameter distributions, a separation between spikelets and fastevents may not be very clear - there are a
# lot of events with amp 1-2mV that have relatively fast rise-time and maxdvdt. Let's start by seeing only events with
# large maxdvdt:
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.225))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
# Looks like this group of events consists of smaller, single fastevents (amp up to 4.8mV) and larger compound fastevents.
# Let's split them out and see:
# singleneuron_data.plot_depolevents((events_underinvestigation & (des_df.amplitude < 4.8)),
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# Indeed, events with amp < 4.8mV are definitely fastevents (beautifully identical normalized waveforms), whereas
# events with amp > 4.8 look more compound - they don't seem to consist of multiple fastevents so much, it's more that
# the up-stroke consists of many noisy depolarizations... But I'll label them as compound anyway:
# fastevents = events_underinvestigation & (des_df.amplitude < 4.8)
# compound_events = events_underinvestigation & (des_df.amplitude > 4.8)
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# In the now remaining events there should be one more group of fastevents, if only because the amplitude of remaining
# events goes up to 4mV (while staying within rise-time/maxdvdt parameter ranges we think of as beloning to fastevents).
# There seems to be a separation between groups of events with amp ~2-4mV, and the rest of events with amp < 2mV. Let's see:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 2.25))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# This looks like the right division, even if these events' normalized waveform differs a bit from events marked
# previously as fastevents: their waveforms are exactly identical to each other, and they all occur together in a pretty
# restricted period of the recording so I'll assume that the change in shape has something to do with change in
# recording conditions. The rest of events are too small&noisy to say with certainty that they would be fastevents,
# so I will leave them be.
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# neuron has terrible baselineV (~-30mV with -2nA DC) throughout recordings; not labeling neat events.