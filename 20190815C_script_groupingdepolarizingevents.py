# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190815C'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Not a great recording at all: neuron is getting held with lots of -DC for large parts of the recording, and resting
# at ~-20mV without it. Injection of current pulses (-1nA - +0.7nA) shows no evidence of t-type Ca or sodium channels
# being active, yet neuron is oscillating with small amp and doing lots of fast-events throughout.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise

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
# des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('aps parameter distributions')

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

# scatters of events parameters:
# fast-events
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
# %% summary plots - neat events only:
nbins = 100  #
neat_events = singleneuron_data.depolarizing_events.neat_event
# fast-events
singleneuron_data.plot_depolevents((fastevents & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events'
                                   )
des_df[(fastevents & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                        'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                        bins=nbins)
plt.suptitle('fast-events, neat ones only')

# compound events
singleneuron_data.plot_depolevents((compound_events & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat compound events'
                                   )
des_df[(compound_events & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                             bins=nbins)
plt.suptitle('compound events, neat ones only')

# aps
# singleneuron_data.plot_depolevents((aps & neat_events),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' neat aps'
#                                    )
# des_df[(aps & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                                              'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                              bins=nbins)
# plt.suptitle('aps, neat ones only')


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# highly variable recording, cell clearly not very happy to begin with but also seal issues
# just one long trace recorded for this neuron, so using that for seeing the events-extraction.
# Recording really is rather noisy, increasing min_depolspeed to 0.3 to get only points that clearly rise above the
# noise in the event-detect-derivative trace, and increasing min_depolamp to 0.5 (honestly, everything with amp<1mV
# mostly just looks like noise).
# block_no = 0
# segment_no = 0
# time_slice = [550, 650] #  [100, 250]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     min_depolamp=0.5,
#                                     min_depolspeed=0.3,
#                                     oscfilter_lpfreq=10,
# )


# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.5,
#                                                      min_depolspeed=0.3,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such
# notes:
# no ttl-triggered experiments performed for this neuron.

# Seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# events with ridiculously depolarized baselinev are for real: they're sitting on top of current pulses that
# depolarize the neuron even to positive potentials (yet it never fires a spike).

# plotting events parameters:
# possibly_spontfastevents_df = des_df[unlabeled_spont_events]
# possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )

# 1. It may not be the neatest recording, but from the rise-time/amplitude scatter it's clear that there are at least
# 4 groups, with amps ~2, 4, 7 and 11mV and rise-time between 0.5 and 1.5ms. So let's start by seeing these 'obvious'
# ones:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 2) & (des_df.rise_time_20_80 <= 1.5))
# interesting: the largest group of events (9 < amp < 12 mV) are in fact all compound ones, while it looks like all the
# rest may be single. The interesting part is that the compound ones seem to occur only at a more hyperpolarized
# baselinev. Anyway, let's label these events:
# compound_events = (events_underinvestigation & (des_df.amplitude > 9))
# fast_events = (events_underinvestigation & (des_df.amplitude < 9))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2a. In the now remaining events, there's a clear cluster of events that stands out for its fast rise-time (~1ms)
# relative to amplitude (~1-2mV); and there are a handful with relatively large amplitude (~2mV, one with amp 4mV)
# and rise-time of 2-3ms, that might still be fast-events. Let's see these first:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 1) & (des_df.rise_time_20_80 > 1.5))
# The two larger ones of these (>1.8mV) are in fact currentpulsechanges (turning tuning pulses up while they're
# happening), while the smaller ones are all things that do not stand out, to my eye, from among the noise/ongoing
# oscillations and small events in the recording. So, I'll label the larger ones and leave the smaller things be:
# currenpulsechanges = (events_underinvestigation & (des_df.amplitude > 1.8))
# singleneuron_data.depolarizing_events.loc[currenpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()

# 2b. Now let's see what's up with the small fast-events:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 0.9) & (des_df.rise_time_20_80 < 1.5))
# OK, from here it's pretty clear that all those events with surprisingly fast maxdvdt are in fact noiseevents (that
# weird negative noise that's sometimes in my recordings). Let's isolate those and label them as noiseevents:
# noiseevents = (unlabeled_spont_events & (des_df.maxdvdt > 0.08))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# That definitely didn't catch them all; but first let's see if we now got fast-events only left in this group:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 1.1) & (des_df.rise_time_20_80 < 1.5))
# now that's them - the two events with amp<1mV were too noisy to make anything of. Let's label them:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3. Let's take one final look at smaller events, to see whether there are still any obvious fast-events or noiseevents
# that should get labeled as such:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude > 0.8))  # those could all be anything - not definitely noise, but definitely too noisy to tell whether they're fast-events or spikelets or what
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.05))
# possibly there's a small group of fast-events in there, but they're very small (~0.5mV) and noisy (baselinev all over
# the place) and occurring only at very hyperpolarized baselinev (~-90mV); indistinguishable from other events by
# parameters. There's also a couple of those fast-negative-noise-things, but they're also very small and don't look so
# numerous as to mess with statistics (a handful on a total of >1000 events).
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )


#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% selecting 5 minutes of best typical behavior and marking 'neat' events
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks('gapFree',
#                                      events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)

# 5 min. of recording from the only recording file, from 1500s to 1800s (these 5 min. cover 3 different holding
# potentials, and the only stretch of recording with the largest-amp fast-events in it).
# block_name = 'gapFree_0000.abf'
# window_start_t = 1500
# window_end_t = 1800
# sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
# trace_start_t = 0
# neat5min_start_idx = (window_start_t - trace_start_t) * float(sampling_frequency)
# neat5min_end_idx = (window_end_t - trace_start_t) * float(sampling_frequency)
# probably_neatevents = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx >= neat5min_start_idx)
#                        & (des_df.peakv_idx < neat5min_end_idx)
#                        )
# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()
