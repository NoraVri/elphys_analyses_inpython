# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190812A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Very nice and interesting recording - neuron changes its behavior a little over the course of time, going from
# small-ish wacky oscillations to large-amp ones. Clearly has fast-events throughout, but frequency decreasing. Clear
# relationship between fast-events occurrence and baselinev: fast-events occur only at baselinev > -51mV (and APs occur
# only > -45mV).

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section 1-3
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section 1
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  # no TTL-applied experiments in this neuron
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

# compound events - there's just the one
# des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                 'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                 bins=nbins)
# plt.suptitle('compound events parameter distributions')

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
# singleneuron_data.plot_depolevents((compound_events & neat_events),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' neat compound events'
#                                    )
# des_df[(compound_events & neat_events)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                                              'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                              bins=nbins)
# plt.suptitle('compound events, neat ones only')

# aps
singleneuron_data.plot_depolevents((aps & neat_events),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=3,
                                   plotwindow_inms=30,
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
# interesting neuron, with wacky oscillations and loads of spont.fast-events; not oscillating for a few minutes when
# first broken into, but also I saw only 1 fast-event there.
# Once blockers get applied, first fast-events go away, then osc amp increases from ~2 to ~8mV for a few minutes and goes back down again.

# I'll use blocks 1 (no blockers, yes oscillations) and 3 (with blockers) to tune get_depolarizingevents parameters.
# I don't see any real reason to change any of the detection values - this is a very lively neuron, all those tiny
# things that get picked up may very well indeed be spikelets.

# block_no = 1
# segment_no = 0
# time_slice = [300, 400]
# #
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     min_depolamp=0.1,
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.1)
# singleneuron_data.write_results()


# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# nbins = 100
# Seeing that light/puff-evoked things all got labeled as such
# notes:
# no ttl-evoked experiments recorded for this neuron (though it does have glu-blockers applied).

# Seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:


# plotting events parameters:
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
# from these plots it seems highly likely that any event with amp>4mV is a fast-event (or a compound one) by rise-time;
# also by maxdvdt there seems to be a grouping, which should help to determine if the events with amp 2-4mV are also fast-events.
# Notably, there looks to be two groups of fast-events - probably something happened in the recording to make it so. Should check.

# 1. First, let's see events with amp>4mV:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 4))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )

# indeed, those look mostly like fast-events, but it's not exactly neat - I think there's a few compound ones in there,
# especially in the largest events/those occurring at more depolarized baselinev. Let's see:
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events under investigation')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='amplitude',
#                                                       spont_subthreshold_depols=events_underinvestigation,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'width_50',
#                                                       cmeasure='amplitude',
#                                                       spont_subthreshold_depols=events_underinvestigation,
#                                                       )
# well, if there are compound events it's not clear from these distributions... Except for the single largest event
# (which stands out by amplitude and rise-time) which is clearly compound (as seen by dVdt/V-plot shape) I do not see
# any reason why these couldn't all be simple fast-events. Labeling them as such:
# compound_event = (events_underinvestigation & (des_df.amplitude > 14))
# fast_events = (events_underinvestigation & ~(des_df.amplitude > 14))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 2. Now let's see events that are <4mV but may still be fast-events:
# In the remaining events there are a handful that stand out for having fast maxdvdt, and fast rise-time (<1ms).
# Let's see them:
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt > 0.15))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# There is one event there of ~0.8mV that seems to have a faster normalized decay waveform than the other events, but
# it does have a very fast rise-time and from looking at it in the raw data trace I can't say that it's a noise-thing
# for any reason, so I will keep it as a fast-event. The other events (1 < amp < 3 mV) are quite by-the-book; decay
# shape is relatively much affected by the ongoing oscillations. Labeling them all as fast-events:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3a. The remaining events definitely don't look all uniformly distributed in their parameters, but it's hard to say
# whether there's really another group of fast-events hiding in there somewhere, even though events still have amp up
# to 2mV. Let's just see any events with amp > 1mV and rise-time < 1.5ms - if there are still fast-events, they will
# be in there.
# events_underinvestigation = (unlabeled_spont_events & (des_df.rise_time_20_80 < 1.5) & (des_df.amplitude >= 1))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# that's actually really clear - most of these are fast-events with identical rise, decays are affected by ongoing
# oscillations. They are separable from the slower-rise events by maxdvdt. Labeling the fast-events:
# fast_events = (events_underinvestigation & (des_df.maxdvdt >= 0.04))
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3b. In fact, let's see just see all events with decent amp (> 1mV) or fast maxdvdt (>0.05mV/ms), to make sure we're
# not missing any that are clearly fast-events:
# events_underinvestigation = (unlabeled_spont_events & (des_df.amplitude >= 1))
# events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt >= 0.05))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# OK, now I'm quite convinced that it won't be possible to find more fast-events in there. (They may be there, but
# unseparable from the mess of other small depolarizing events).

# In fact, looking again at 'neat' events I'm seeing that anything with amp < 2mV is too messy to be definitely
# a fast-event. Re-labeling any fast-events smaller than that:
# not_fastevents = (fastevents & (des_df.amplitude <= 2))
# singleneuron_data.depolarizing_events.loc[not_fastevents, 'event_label'] = np.nan
# singleneuron_data.write_results()
### -- This concludes sorting through depolarizing events and labeling them -- ###
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks('gapFree',
#                                      events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)
# this neuron changes its behavior quite a lot over the course of recordings: starts out not oscillating, then
# oscillations start coming on and off, growing in amplitude and decreasing in wackyness over the course of recordings.
# I think the neuron is on its best behavior in gapFree_0001, where it's oscillating (or at least listening to
# oscillations) throughout and has the highest frequency (by eye) of fast-events and spont.APs, but honestly, it's
# looking quite stable throughout the first three gapFree files; fast-events suddenly drop in maxdvdt (from up to 1
# down to 0.3 mV/ms) once long current pulses are applied.
# probably_neatevents = (des_df.file_origin.str.match(pat='gapFree_0'))
# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()