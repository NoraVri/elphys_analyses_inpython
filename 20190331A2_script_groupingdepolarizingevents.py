# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190331A2'
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
nbins = 100
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Pretty much a twin of A1: not always the nicest recording, but complete with oscs (mostly small amp) and big spikelets
# and lots of fast-events and APs that get evoked from (multiple) fast-events, mostly clearly recognizable despite
# un-ideal and changing recording conditions.
# Neuron is not oscillating to begin with - however, there are no fast-events in this stretch of recording, only APs.


aps = des_df.event_label == 'actionpotential'
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section2-7
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section2-7
smallslowevents = des_df.event_label.isna()

# %%
# summary plots:
# singleneuron_data.plot_depoleventsgroups_overlayed(aps, fastevents, compound_events,
#                                                    group_labels=['APs', 'fastevents', 'compound events'],
#                                                    do_baselining=True,
#                                                    # do_normalizing=True,
#                                                    plot_dvdt=True,
#                                                    )

# aps
# des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
#                          'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
# plt.suptitle('aps')
# singleneuron_data.plot_depolevents(aps, colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' action potentials')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
#                                                       aps=aps)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       aps=aps)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       aps=aps)

# fast-events
des_df[fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
                                'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
plt.suptitle('fast-events')
singleneuron_data.plot_depolevents(fastevents, colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15,
                                   plt_title=' fast-events')
# singleneuron_data.plot_depolevents(fastevents, colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' fast-events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fastevents)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fastevents)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fastevents)

# compound events
des_df[compound_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
                                     'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
plt.suptitle('compound events')
singleneuron_data.plot_depolevents(compound_events, colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15,
                                   plt_title=' compound events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
#                                                       compound_events=compound_events)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       compound_events=compound_events)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       compound_events=compound_events)

# things that are probably spikelets
# des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev', 'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
# plt.suptitle('small, slow events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
#                                                       probably_spikelets=smallslowevents)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       probably_spikelets=smallslowevents)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       probably_spikelets=smallslowevents)
# singleneuron_data.plot_depolevents((smallslowevents & (des_df.amplitude > 1)), colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' small slow events')

# %% plots for publication figures
bins=50
sampling_rate = int(singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate)
probably_neatevents = ((des_df.file_origin == 'gapFree_0000.abf')
                       & (des_df.peakv_idx > (800 * sampling_rate))
                       & (des_df.peakv_idx < (1100 * sampling_rate))
                       )
# %%
# singleneuron_data.plot_rawdatablocks('gapFree_0000', events_to_mark=(fastevents & probably_neatevents))
# it's not so easy for this neuron to find 5 minutes of consecutive recording where conditions don't change too much
# - also this stretch isn't exactly ideal, neuron is being held with -DC to keep a good baselinev; maybe some IV files would be better
singleneuron_data.plot_depolevents((fastevents & probably_neatevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat fast-events'
                                   )
# des_df[(fastevents & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                                         'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                                  bins=bins)
# plt.suptitle('fast-events, neat ones only')
# %%
# neat compound fast-events:
singleneuron_data.plot_depolevents((compound_events & probably_neatevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=15,
                                   plt_title=' neat compound events'
                                   )
des_df[(compound_events & probably_neatevents)].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                                             'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                                 bins=bins)
plt.suptitle('compound events, neat ones only')

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# This neuron has its moments, but overall its not the greatest recording, with recording conditions being quite
# variable in the first 20min. or so, then settling in for a bit until neuron basically dies (IV3 - stops firing APs,
# and needs to be held with progressively more -DC to keep a decent baselinev).
# I will use a time-slice from the end of gapFree_0000 to find good parameters, as this looks like a nice stretch of
# the neuron being on its 'best typical' behavior


# block_no = 0
# segment_no = 0
# time_slice = [2050, 2150]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                                         min_depolamp=0.3,  # it's a quite noisy recording, by eye it's basically impossible to distinguish between events and wobbles maybe even above that amp
#                                                         oscfilter_lpfreq=10,  # oscs coming on intermittently and never seem to go faster than ~6Hz
#                                                         min_depolspeed=0.2,  # everything that's clearly an event to my eyes easily reaches that value, below that it's really just a lot of noise
#                                                         ahp_width_window=200  # 150 may still be mostly OK, but in some cases might just not cut it
# )
# I think it looks OK like this - for events with amp up tp ~0.5mV the algorithm and yosi may disagree sometimes on
# what's an event and what is not, but above that it all looks really good.

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.3,
#                                                      min_depolspeed=0.2,
#                                                      oscfilter_lpfreq=10,
#                                                      ahp_width_window=200)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events


# seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# looks like the algorithm did about as neat a job at picking up events as can be expected from this noisy neuron;
# it'll probably be very worth it to go file-by-file to tease apart what's going on with all the events.
# Interestingly, the neuron is doing barely any fast-events in the first 10min. or so (lots of APs though).

# 1. plotting events parameters to see where to start narrowing down on fast-events:
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# not much of groupings to be seen anywhere, except maybe in the amp and maxdvdt histograms; probably the fact that
# lots of events are compound or otherwise deformed has something to do with it.
# plotting some events:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 6))
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# indeed, lots of these are compound, and lots of them are much rounder than what we expect of a classic fast-event.

# 2. let's start from examining the group of largest-amp events (most events have amp up to 10mV, only about a dozen
# have amp > 12mV)
# largeamp_events = (possibly_spontfastevents & (des_df.amplitude > 12))
# singleneuron_data.plot_depolevents(largeamp_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# OK these are all compound events, it's very clear both from the raw waveform and the dvdt/V plot
# labeling them as such:
# singleneuron_data.depolarizing_events.loc[largeamp_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# 3. in the remaining events, there are tons with short rise-time (<1ms, shorter than for compound events) but
# relatively few events with large maxdvdt. Let's see a scatter of rise-time vs maxdvdt:
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='amplitude',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# OK, that's starting to look like there's some structure to this madness. There's clearly a section of events with
# fast rise-time (up to ~1ms) where increasing dVdt correlates with increasing event amplitude, and it seems that
# events with amp>6mV often have twice as long rise-time than that (presumably they are double events).
# So let's see only events >6mV, maybe it'll be easy to tell apart compound ones and single ones:
# largeamp_events = (possibly_spontfastevents & (des_df.amplitude > 6))
# singleneuron_data.plot_depolevents(largeamp_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[largeamp_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# Looks like there's not in fact all that many compound events here, just lots of 'degenerate' ones that look wider
# and rounder than the classic fast-event. But there's also definitely a group of very neat fast-events in there with
# narrower width (2.5 - 4ms), and this division is pretty clear from the width_50-histogram, too
# probably_neatlargefastevents = (largeamp_events & (des_df.width_50 < 4))
# singleneuron_data.plot_depolevents(probably_neatlargefastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' probably neat fast-events'
#                                    )
# des_df[probably_neatlargefastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# plt.suptitle('probably neat fast-events')
# actually, most of these are still compound events, looks like only at the lowest baselinev we get single events:
# lowbaseline_largeampevents = (probably_neatlargefastevents & (des_df.baselinev < -52))
# singleneuron_data.plot_depolevents(lowbaseline_largeampevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' low baselinev events'
#                                    )
# largeamp_probablycompoundevents = (probably_neatlargefastevents & (des_df.baselinev >= -46))
# singleneuron_data.plot_depolevents(largeamp_probablycompoundevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    )
# It's true that the low-baselinev events are all single ones, but then there's a region of baselinev where both single
# and compound events occur (and some of the single events are rather wide so everything overlaps).
# Let's first just label the events that are definitely fast-events or definitely compound events:
# singleneuron_data.depolarizing_events.loc[lowbaseline_largeampevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[largeamp_probablycompoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# 4. looks like there's nothing better to do than go over all events in narrow amplitude ranges, and tease apart
# compound events and single events by whatever makes most sense.
nbins = 40  # I'm gonna be taking about a dozen events at the time
# 4a. events > 8mV:
# there's three compound events in there; two of them look like they're the ones with the longest rise-time
# compound_events = (largeamp_events & (des_df.rise_time_20_80 > 2))
# singleneuron_data.plot_depolevents(compound_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# indeed; labeling them as such:
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# now the remaining compound-event is the one with the lowest baselinev and narrowest width (consistent with recording quality deteriorating for the other ones)
# compound_event = (largeamp_events & (des_df.baselinev < 47.5))
# labeling it as such:
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# The now remaining largeamp events are all single fast-events (rise-time up to 1.5ms), labeling them as such:
# singleneuron_data.depolarizing_events.loc[largeamp_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 4b. events > 7mV:
# one of these events doesn't decay at all - as seen in raw data trace, it's just part of the neuron dying.
# Labeling it as noiseevent:
# noiseevent = (largeamp_events & (des_df.width_50.isna()))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# in the remaining events there's just one that clearly looks compound, I think it's the single widest one:
# compound_event = (largeamp_events & (des_df.width_50 > 8))
# indeed - labeling it as such:
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# The remaining events of this amplitude all look like fast-events - all have rise-time < 1.5ms. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[largeamp_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# It's still just too messy... From here on out I'll narrow down also by baselinev/recordingfile
# 4c. events > 6mV:
# amp_cutoffvalue = 6
# recordingfile = 'IV'#'gapFree' #'gapFree_0000.abf'
# largeamp_events = (possibly_spontfastevents
#                    & (des_df.amplitude > amp_cutoffvalue)
#                    & (des_df.file_origin.str.contains(recordingfile)))
#
# singleneuron_data.plot_depolevents(largeamp_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[largeamp_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'width_70', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# in gapFree_0000:
# that looks like it's mostly wider fast-events and compound events, but with a few neat fast-events mixed in that
# should be easy to separate out by their width_50 value. Let's see:
# probably_neatfastevents = (largeamp_events & (des_df.width_50 < 4))
# singleneuron_data.plot_depolevents(probably_neatfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True)
# not quite - there's a few double events there, but their maxdvdt value is smaller. Let's see that these are all
# neat events now:
# probably_neatfastevents = (largeamp_events & (des_df.width_50 < 4) & (des_df.maxdvdt > 0.32))
# singleneuron_data.plot_depolevents(probably_neatfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True)
# indeed. Labeling them as such :
# singleneuron_data.depolarizing_events.loc[probably_neatfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# and looks like in the remaining events, the compounds and the singles can be separated by rise-time. Let's see:
# probably_neatfastevents = (largeamp_events & (des_df.rise_time_20_80 < 1))
# singleneuron_data.plot_depolevents(probably_neatfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' probably fastevents')  # indeed, these are all singles by the dVdt/V-plot shape; though some of them do have a tiny foot (<1mV) before the main event
# probably_compoundevents = (largeamp_events & (des_df.rise_time_20_80 > 1))
# singleneuron_data.plot_depolevents(probably_compoundevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' probably compound events')  # indeed, these are all compound by the dVdt/V-plot shape.
# labeling them as such:
# singleneuron_data.depolarizing_events.loc[probably_neatfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[probably_compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# in the other gapFree files there are no longer any events with amp>6mV; in IV-files all events look like singles,
# also when I decrease the amp cutoff. Let's see how low we can go with all events still having the fast rise-time:
# amp_cutoffvalue = 2
# recordingfile = 'IV'
# largeamp_events = (possibly_spontfastevents
#                    & (des_df.amplitude > amp_cutoffvalue)
#                    & (des_df.file_origin.str.contains(recordingfile)))
#
# singleneuron_data.plot_depolevents((largeamp_events & (des_df.rise_time_20_80 < 2)),
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[largeamp_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'width_70', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# going all the way down to 2mV amp I get a single event that has rise-time>3ms that is clearly a compound event,
# all other events have rise-time <1.5ms and look identical enough to me to all be fast-events.
# labeling them as such:
# fastevents = (largeamp_events & (des_df.rise_time_20_80 < 2))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# compound_events = (largeamp_events & (des_df.rise_time_20_80 > 2))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# 4d. let's deal with all the remaining unlabeled events in gapFree_0000, by amplitude group:
# amp_cutoffvalue = 3 #3.5 #4 #4.5 #5
# recordingfile = 'gapFree_0000.abf'
# largeamp_events = (possibly_spontfastevents
#                    & (des_df.amplitude > amp_cutoffvalue)
#                    & (des_df.file_origin.str.contains(recordingfile))
#                    )
#
# singleneuron_data.plot_depolevents(largeamp_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[largeamp_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'width_70', 'amplitude', 'baselinev'],
#                              bins=nbins,)
#
# probably_fastevents = (largeamp_events & (des_df.rise_time_20_80 < 1.6))
# probably_compoundevents = (largeamp_events & (des_df.rise_time_20_80 >= 1.6))
# for events with amp>5mV, cutting by rise-time at 1.5ms (there's a clear gap there in the histogram) gives us the
# groups of single and compound events.
# for events with amp>4.5mV, the same rise-time cutoff works - there's one event (amp~4.6mV) with a kinda slow decay
# among the fast-events, but it's not clearly a compound event so I'll keep it in this group.
# for events with amp>4mV, all seem to be single fast-events - rise-time is never >1.4ms, and even though there are a
# handful with somewhat more deformed rise/decay shapes than we might like they are not clearly compound so I'm keeping
# them in this group.
# probably_fastevents = largeamp_events
# for events with amp>3.5mV, the rise-time cutoff needs to be at 1.2ms - events with rt>1.2 are clearly compound.
# Though I've got to say, at this point for some events it's really hard to say whether they are simply wider, or have
# a spikelet or another fast-event riding them...
# for events with amp>3mV, only events with rise-time>1.6ms are clearly compound, but I'm not so sure that the rest
# should all be counted as fast-events (perhaps they are big spikelets, fitting in with the parameter distributions of those).
# So I'll label only the compound events for now
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[probably_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[probably_compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# singleneuron_data.plot_depolevents(probably_fastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title='probably fast-events'
#                                    )
#
# singleneuron_data.plot_depolevents(probably_compoundevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title='probably compound events'
#                                    )

# 5. Let's go back to seeing events from all recording files, and decide which events are small, slow events.
# From the parameters histograms and scatters of all as-yet unlabeled events, there isn't a clean break anywhere; we'll probably
# have to use an intersection of amplitude, rise-time and maxdvdt parameters to delineate the group of smallslowevents.
# Let's see what that looks like:
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='maxdvdt',
#                                                       possibly_spontfastevents=possibly_spontfastevents,
#                                                       )
# Ok, this is starting to look like there's some structure to the madness. Clearly there's a group of events with
# rise-time that is very fast relative to their amplitude (<1ms / 1.5-3.5mV), and a dense cloud of what are probably
# small, slow events with amp up to 1.5mV. And then there's a few dozen events (amp > 1.5mV, rise-time>1ms) that we'll
# have to see to decide what they are.

# Now, seeing events marked in the raw data it's clear that in gapFree_0002 there's no real events anymore, it's all just
# too noisy - so I'm labeling all "events" picked up in there as noiseevents:
# noiseevents = des_df.file_origin == 'gapFree_0002.abf'
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# In fact, it's true also for the shortPulse recording files that the traces are simply too noisy to pick up anything
# useful - maybe here and there something could be a spikelet/fast-event if we squint our eyes right, but with
# -700pA - -1200pA to keep baselineV ~-40 I don't see why all events from these traces shouldn't just be excluded.
# noiseevents = des_df.file_origin.str.contains('shortPulse')
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# 5a. First, let's split any remaining events out by amplitude and see if <1.5mV we don't see a grouping indicative of fast-events:
# smallslowevents = (unlabeled_events & (des_df.amplitude <= 1.5))
# singleneuron_data.plot_depolevents(smallslowevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' probably spikelets'
#                                    )
# des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# plt.suptitle('probably spikelets')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       smallslowevents=smallslowevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       smallslowevents=smallslowevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='baselinev',
#                                                       smallslowevents=smallslowevents,
#                                                       )
# hmm, I'm still not sure - it's long-tailed distributions in the histograms and mostly just clouds in the scatters,
# except for the maxdvdt/amp scatter which shows some relatively small (~0.4mV) events with high maxdvdt
# (0.1 - 0.35mV/ms, while most points barely reach 0.1mV/ms). Let's see these events:
# events_underinvestigation = (smallslowevents & (des_df.maxdvdt >= 0.1)
#                              # & (des_df.amplitude > 1)
#                              )
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly fast-events'
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# plt.suptitle('')
# ah I see now - most of these are 'events' starting with that weird, fast negative noise that was creeping into my
# recordings, that's why they have high maxdvdt value but otherwise small amp. However, there are a few events there
# that are actually large&fast enough to possibly be fast-events.
# So let's first see that we grab all the negative-noise 'events' and label them as such:
# noiseevents = (events_underinvestigation & (des_df.amplitude < 1))
# singleneuron_data.plot_depolevents(noiseevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' probably noiseevents',
#                                    newplot_per_event=True
#                                    )
# There are just 4 events in there (out of 78) that do NOT clearly contain the negative-noise thing - none of these 4
# are very nice or neat events though, so I'm OK lumping them in with the noise. Labeling as such:
# singleneuron_data.depolarizing_events.loc[noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# 5b. another few rounds of filtering out noisy events like that:
# events_underinvestigation = (smallslowevents & (des_df.maxdvdt >= 0.06)
#                              # & (des_df.amplitude < 0.4)
#                              )
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly fast-events',
#                                    # newplot_per_event=True,
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# for events with maxdvdt>0.08 & amplitude < 0.8, just 3 events there (out of 36) that do NOT clearly contain the
# negative-noise thing, but once again none of these 3 are particularly good-looking events so I don't think they'll be missed if they get labeled as noise.
# for events with maxdvdt>0.07 & amplitude <0.4, just 1 event there (out of 13) does NOT clearly have the negative
# noise-thing, but once again this event is very small (<0.3mV) and also otherwise noisy and I doubt it will be missed.
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# for events with maxdvdt>0.06 there are still some with that negative noise preceding the event, but the noise is
# now very small (up to ~0.4mV amplitude) and much more negligible compared to the size of events (0.2 - 2mV amp).
# So, I will consider all remaining events to be real.

# 6. returning again to all as-yet unlabeled events, let's now see the group with the smallest maxdvdt values: in
# the histogram there's a clear peak of events with mean maxdvdt ~0.04, declining steeply to ~0.08, and my feeling is
# that these are all gonna be spikelets. Let's see:
# smallslowevents = (unlabeled_events & (des_df.maxdvdt <= 0.08))
# singleneuron_data.plot_depolevents(smallslowevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' probably spikelets'
#                                    )
# des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# plt.suptitle('probably spikelets')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       smallslowevents=smallslowevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       smallslowevents=smallslowevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='baselinev',
#                                                       smallslowevents=smallslowevents,
#                                                       )
# we still got a couple of events in there with pretty fast rise-time (<2ms) and large amplitude (>2mV), let's see them:
# indeed, these look like fast-events - the normalized waveforms are rather identical, with decay shape changing
# a bit for different baselinev. Some of these events look kinda compound with a spikelet, but not so much so that they
# would muck up the stats of the single fast-events. So I'll label them as such:
# singleneuron_data.depolarizing_events.loc[possibly_notsmallslowevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 6a. now let's see if there are any events among those with amp<2mV that should clearly be counted as fast-events:
# possibly_notsmallslowevents = (smallslowevents & (des_df.rise_time_20_80 < 2)
#                                & (des_df.amplitude > 1)
#                                & (des_df.amplitude <=1.5))
# singleneuron_data.plot_depolevents(possibly_notsmallslowevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly not spikelets'
#                                    )
# des_df[possibly_notsmallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# in the events with amp>1.5mV, there are just a handful that look wider than the rest, and the narrower ones could
# easily all be fast-events:
# probably_spikelets = (possibly_notsmallslowevents & (des_df.width_50 >= 6))
# singleneuron_data.plot_depolevents(probably_spikelets,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly not spikelets'
#                                    )
# probably_fastevents = (possibly_notsmallslowevents & (des_df.width_50 < 6))
# singleneuron_data.plot_depolevents(probably_fastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly not spikelets'
#                                    )
# yea that looks right - the wider events are also from earlier on in the recording, and have different peak shape
# and longer decay than the fast-events. Labeling the fast-events as such:
# singleneuron_data.depolarizing_events.loc[probably_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# in the events with 1<amp<1.5mV, we may still have a group of fast-events - those with the smaller widths (there's a break in the histogram there):
# possibly_fastevents = (possibly_notsmallslowevents & (des_df.width_50 < 7))
# singleneuron_data.plot_depolevents(possibly_fastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly not spikelets'
#                                    )
# des_df[possibly_fastevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
#                                                         'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
#                                                  bins=bins)
# I'm really not sure what to do here - the parameter distributions very much match those of neat fast-events found
# so far (plus some added measurement noise simply because events are so small), but I'm afraid Yosi will yell if I
# categorize these as fast-events. So I will leave these for now, and decide later. TODO

# %%
# 7. returning yet again to all as-yet unlabeled events, let's now see the group with amp>1.5mV: since it's with events
# below this value that we start running into real problems deciding what are fastevents and what aren't, above this
# value it should be easy to make the call. Let's see:
# events_underinvestigation = (possibly_spontfastevents & (des_df.amplitude > 1.5))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly fast-events'
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# some of these may be compound, but all in all it looks like all of these could easily be fast-events. Let's go over
# them by baselinev ranges and see:

# baselinevrange = [-60, -90]  #[-55, -60]  #[-50, -55]  #[-45, -50]  #[-40, -45]  #[-35, -40]  #[-30, -35]
# baselinevrange_events = (events_underinvestigation
#                          & (des_df.baselinev < baselinevrange[0]) & (des_df.baselinev >= baselinevrange[1])
#                          )
# singleneuron_data.plot_depolevents(baselinevrange_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly fast-events'
#                                    )
# des_df[baselinevrange_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# events with baselinerange = [-30, -35]: about half of them are clearly compound, the rest single, separable by
# rise-time. Labeling them as such:
# fastevents = (baselinevrange_events & (des_df.rise_time_20_80 <= 1))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# compound_events = (baselinevrange_events & (des_df.rise_time_20_80 > 1))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# events with baselinerange = [-35, -40]: I can only conclude they are all fast-events - waveforms are definitely not
# perfect, but that seems to be due to recording conditions changing (not compoundness or anything like that).
# Labeling them as such:
# fastevents = baselinevrange_events
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinerange = [-40, -45]: cannot but conclude that these are all fast-events, except for two that have
# slower maxdvdt than all the rest and another two that have wider decay than all the rest (they may just be outliers,
# but with 1.5>amp>2mV they may also very well be spikelets). Labeling the fast-events:
# fastevents = (baselinevrange_events & (des_df.width_50 < 7) & (des_df.maxdvdt > 0.05))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinerange = [-45, -50]: there are pretty clear amplitude groups here, using that to narrow down:
# amplituderange_baselinerange_events = (baselinevrange_events & (des_df.amplitude < 2))
# in this group, events with width > 8 look to have a different shape - they also have slower rise-time (>1.5ms) than
# most of the rest of the events. One event with rise-time > 2 is a compound event (small slow event preceding). Labeling:
# fastevents = (amplituderange_baselinerange_events & (des_df.width_50 < 8) & (des_df.rise_time_20_80 < 2))
# compound_events = (amplituderange_baselinerange_events & (des_df.width_50 < 8) & (des_df.rise_time_20_80 > 2))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# amplituderange_baselinerange_events = (baselinevrange_events & (des_df.amplitude >= 2) & (des_df.amplitude < 3))
# played around with these quite a bit - there's 3 events that look to me like they might be compound because they are
# very wide (as though two events of the same amplitude occurring with <1ms apart), but a double peak is not evident
# from the dVdt/V plot and the rise and decay shape fit with the other events, so I will label them all as fastevents.
# singleneuron_data.depolarizing_events.loc[amplituderange_baselinerange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# amplituderange_baselinerange_events = (baselinevrange_events & (des_df.amplitude >= 3))
# no question about it, these are all fast-events.
# singleneuron_data.depolarizing_events.loc[amplituderange_baselinerange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# singleneuron_data.plot_depolevents(amplituderange_baselinerange_events,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True,
#                                    plt_title=' possibly fast-events'
#                                    )
# des_df[amplituderange_baselinerange_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                              bins=nbins,)
# events with baselinerange = [-50, -55]: all except one event (recognizable by different decay shape) look like
# fast-events to me. Labeling them as such:
# fastevents = (baselinevrange_events & (des_df.width_50 > 8))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinerange = [-55, -60]: no question about it, these are all fast-events.
# singleneuron_data.depolarizing_events.loc[baselinevrange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinerange = [-60, -90]: no question about it, these are all fast-events.
# singleneuron_data.depolarizing_events.loc[baselinevrange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

#### this concludes sorting through all events and labeling them ####
# (except for among events <1.5mV, where there may still be a group of fast-events not labeled as such - see section6).
