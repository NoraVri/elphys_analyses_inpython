# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20210124A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# this neuron has LOADS of fast-events, and gets held with DC current to see baselinev effect on frequency
# has small, wacky oscillations off and on, should be interesting to see if that correlates with fast-events somehow.
# Another noteworthy feature: this neuron has a few double-events, where the second event happens about halfway through
# the decay-phase of the first one (very unlike the double up-stroke that we usually see); the second event's half-width
# is significantly shorter than that of a regular fast-event.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  #

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
singleneuron_data.plot_depolevents((aps & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat aps'
                                   )
des_df[(aps & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                             bins=nbins)
plt.suptitle('aps, neat ones only')

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:

# block_no = 1 # 0
# segment_no = 0
# time_slice = [0, 100]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                                                     min_depolamp=0.1,
#                                                                     min_depolspeed=0.2,  # it's the right setting for catching only events that rise above the noise, also by amp in the event-detect trace
#                                                                     ttleffect_window=5,  # response to light very small but immediate
#                                                                     ahp_width_window=200,  # 150 looks OK for the most part, but borderline for some APs so increasing a bit
#                                                                     oscfilter_lpfreq=10,  # oscs are ~7Hz but very small amp so this should do
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.1,
#                                                      min_depolspeed=0.2,
#                                                      ttleffect_window=5,
#                                                      ahp_width_window=200,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# interesting - early on it looks like the light may be activating a proper fast-event twice (4, 2mV) but especially
# later on, a very small (~1mV) response shows up consistently. It gets picked up by the algorithm quite nicely for the
# most part, though not on every light application - but also, sometimes the light seems to just have no effect.

# Seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:
# events <0.5mV I'm not sure all got picked up, but generally it looks great.

# plotting all as-yet unlabeled events parameters:
# des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
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
#                                                       cmeasure='amplitude',
#                                                       spont_subthreshold_depols=unlabeled_spont_events,
#                                                       )
# Labeling fast-events and other events fitting in categories not labeled automatically (fastevent, compound_event, other_event, noiseevent)
# 1. From the distributions, it looks like for the most part it should be fairly straightforward to filter fast-events
# from the other things by rise-time/amplitude/maxdvdt: aside from a few outliers, most events with amp >2.5 look like
# they should be fast-events, though from the rise-time distribution it looks like there may also be a lot of compound
# events included especially in the events with larger amps (>10mV).
# From plotting all events >2.5mV together it would seem that I'm right; definitely mostly fast-events, but also for
# sure some compound ones in there. Let's just start going over them by amplitude group, starting with the largest:

# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 14))
# 1a. from among these, the few with the smallest maxdvdt values are compound events:
# compound_events = (events_underinvestigation & (des_df.maxdvdt <= 0.4))
# in the remaining events, at more hyperpolarized baselinev we have only compound events:
# compound_events2 = (events_underinvestigation & (des_df.maxdvdt > 0.4) & (des_df.baselinev < -55))
# compound_events = (compound_events | compound_events2)
# and at more depolarized baselinev we have only single events (except for the one with the long rise-time):
# fast_events = (events_underinvestigation & (des_df.maxdvdt > 0.4)
#                                             & (des_df.rise_time_20_80 < 1) & (des_df.baselinev > -50))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 1b. In the remaining events, those with rise-time >= 0.7ms are all compound (or made to look compound by some noise):
# compound_events = (events_underinvestigation & (des_df.rise_time_20_80 >= 0.7))
# and in the events with rise-time < 0.7ms, the handful with the lowest baselinev are also compound; the rest are
# regular fast-events:
# compound_events2 = (events_underinvestigation & (des_df.rise_time_20_80 < 0.7) & (des_df.baselinev <= -53.5))
# compound_events = (compound_events | compound_events2)
# fast_events = (events_underinvestigation & (des_df.rise_time_20_80 < 0.7) & (des_df.baselinev > -53.5))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2. Moving on to the next amplitude group: events > 10mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 10))
# 2a. the handful of events with the smallest maxdvdt values are mostly compound,
# as well as some others - this gets a bunch of them:
# compound_events = (events_underinvestigation & (des_df.maxdvdt < 0.58) & (des_df.baselinev <= -57))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 2b.
# fastevents = (events_underinvestigation & (des_df.maxdvdt < 0.4))  # that's not all of them, but quite some
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 2c.
# compound_events = (events_underinvestigation & (des_df.rise_time_20_80 > 0.7))  # that's not all of them, but quite some
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# 2d. now at more depolarized baselinev there's practically only simple fast-events, except for one that has a clear
# 'foot' of ~2mV:
# compound_event = (events_underinvestigation & (des_df.baselinev >= -54) & (des_df.rise_time_10_90 > 2))
# fastevents = (events_underinvestigation & (des_df.baselinev >= -54) & (des_df.rise_time_10_90 < 2))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 2e. interestingly, the now remaining events seem separable by width_50, such that fast-events have larger width there
# than compound events (maybe the distinction isn't exactly perfect, but it looks like the best one to me).
# compound_event = (events_underinvestigation & (des_df.width_50 < 2.7))
# fastevents = (events_underinvestigation & (des_df.width_50 >= 2.7))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3. Moving on to the next amplitude group: events > 7.5mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 7.5))
# OK then - some of these are very obviously compound, others maybe less so, but the vast majority of these are
# single fast-events.
# 3a. First let's tackle the small group of events with much smaller maxdvdt than the rest:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 7.5) & (des_df.maxdvdt < 0.4))
# two are compound, the rest are not, clearly separable by rise-time
# compound_events = (events_underinvestigation & (des_df.rise_time_20_80 > 1))
# fast_events = (events_underinvestigation & (des_df.rise_time_20_80 < 1))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 3b. In the remaining events I do not see much indication for compound ones, except for one place where a second event
# arrives just as a first one is about half-way decayed (the decay shape of the second event is clearly affected) and
# one that looks similar, but only the second peak of the event got picked up giving it a much longer rise-time than the others.
# compound_event = (events_underinvestigation & (des_df.width_50 < 2))
# compound_event2 = (events_underinvestigation & (des_df.rise_time_20_80 > 2))
# compound_events = (compound_event | compound_event2)
# fast_events = (events_underinvestigation & ~compound_events)
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 4. Moving on to the next amplitude group: events > 5.5mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 5.5))
# Don't really see any indications that there would be many (if any) compound events here; there's a few events that
# have a small slow depolarization riding their decay-phase but it doesn't look like that would affect measurements much.
# compound_event = (events_underinvestigation & (des_df.maxdvdt > 0.25) & (des_df.maxdvdt < 0.3))
# fast_events = (events_underinvestigation & ~compound_event)
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 5. Moving on to the next amplitude group: events > 4mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 4))
# Don't really see much indication for compound events here either, except for two that are significantly less wide
# than the rest - one of these is an event riding the decay-phase of another event, the other one is riding a
# rebound potential.
# event_on_reboundpotential = (events_underinvestigation & (des_df.width_50 < 2)
#                              & (des_df.file_origin == 'longPulses_0000.abf'))
# compound_event = (events_underinvestigation & (des_df.width_50 < 2)
#                              & (des_df.file_origin == 'shortPulse_0001.abf'))
# fast_events = (events_underinvestigation & ~(compound_event | event_on_reboundpotential))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[event_on_reboundpotential, 'event_label'] = 'fastevent_on_reboundpotential'
# singleneuron_data.write_results()

# 6. Moving on to the next amplitude group: events > 1.5mV
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 1.5))
# 6a. some of these are definitely fast-events, amp~3.5mV; interestingly they mostly seem to occur at rather hyperpolarized
# (<-70mV) baselinev. But there's also some noise-things here, and I'll want to take a closer look at the rest of the
# events (most definitely a lot of spikelets there and I don't think it'll be possible to fish out more fast ones,
# but who knows).
# noiseevents = (events_underinvestigation & (des_df.maxdvdt > 0.15) & (des_df.baselinev > -49))
# fastevents = (events_underinvestigation & (des_df.maxdvdt > 0.15) & (des_df.baselinev <= -49))
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 6b. I looked some more at the remaining events, but even those with the fastest maxdvdt and the largest amplitudes
# (there are still two events with amp ~3.5mV) look more like (compound) spikelets to me than fast-events.

# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
#
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')
#
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       events_underinvestigation=events_underinvestigation,
#                                                       )

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% selecting 5 minutes of best typical behavior and marking 'neat' events
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks('gapFree',
#                                      events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)

# file gapFree_0002 has nice long stretches of recording where the neuron is held with - or + DC to change baselinev;
# picking a few stretches of 30 - 60s to catch them all.
# block_name = 'gapFree_0002.abf'
# sampling_frequency = singleneuron_data.blocks[2].channel_indexes[0].analogsignals[0].sampling_rate
# window1_start = (940 * sampling_frequency)
# window1_end = (1030 * sampling_frequency)  # 90s at baselinev
# probably_neatevents1 = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx > window1_start)
#                         & (des_df.peakv_idx < window1_end))
# window2_start = (1400 * sampling_frequency)
# window2_end = (1490 * sampling_frequency)  # 90s at depolarized v
# probably_neatevents2 = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx > window2_start)
#                         & (des_df.peakv_idx < window2_end))
# window3_start = (2260 * sampling_frequency)
# window3_end = (2320 * sampling_frequency)  # 60s at two different hyperpolarized baselinevs
# probably_neatevents3 = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx > window3_start)
#                         & (des_df.peakv_idx < window3_end))
# window4_start = (2050 * sampling_frequency)
# window4_end = (2110 * sampling_frequency)  # 60s at two different hyperpolarized baselinevs
# probably_neatevents4 = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx > window4_start)
#                         & (des_df.peakv_idx < window4_end))
# probably_neatevents = (probably_neatevents1 | probably_neatevents2 | probably_neatevents3 | probably_neatevents4)
# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()

# %%

