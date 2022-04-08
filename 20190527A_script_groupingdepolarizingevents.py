# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190527A'
singleneuron_data = SingleNeuron(neuron_name)

des_df = singleneuron_data.depolarizing_events
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# all the kinds of interesting events detected in this neuron:
aps = des_df.event_label == 'actionpotential'
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section3-
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section3-
spont_events = ~des_df.applied_ttlpulse
smallslowevents = (des_df.event_label.isna() & spont_events)  # see plots and analyses section2,

# %% summary plots - all spontaneous events:
# histogram of baselinev in the entire recording:
# singleneuron_data.get_timespentrecording(make_baselinev_hist=True)
# histograms of events parameters
nbins = 150
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
# %% summary plots - neat spontaneous events only:
nbins = 100  #
neat_events = singleneuron_data.depolarizing_events.neat_event
# %%
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
# %% plots: subtracting single events from compound ones
events_4mVgroup = (neat_events & fastevents & (des_df.amplitude > 3.8) & (des_df.amplitude < 4.8))
compoundevents_group = (compound_events & (des_df.amplitude > 8) & (des_df.amplitude < 9.25))
singleneuron_data.plot_depoleventsgroups_averages(compoundevents_group, events_4mVgroup,
                                                  group_labels=['compound', 'single'],
                                                  subtract_traces=True,
                                                  # delta_t=0.5
                                                  )

# %% plots: light-evoked activity
# singleneuron_data.plot_rawdatatraces_ttlaligned(newplot_per_block=True)

# blocks that are identical in light intensity & spot size:
# 2-3% - _1 and _5
# 5% - _0
# 10% - _2 and _3
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0002', 'light_0003')
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0000')
singleneuron_data.plot_rawdatatraces_ttlaligned('light_0001', 'light_0005')
# %%
#wholefield:
# variable - _0 - _12
# 10% - _15 - 21
blocknames_list = singleneuron_data.get_blocknames(printing='off')
blocknames = []
for i in range(15,21):
    blocknames += [name for name in blocknames_list if str(i) in name]
singleneuron_data.plot_rawdatatraces_ttlaligned(*blocknames, 'light_0002', 'light_0003', newplot_per_block=False)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# This neuron's got LOADS of events, by eye starting at ~2mV but also lots of big, very clear ones.
# Neuron is mostly holding steady throughout recordings (though some evidence of electrode drift here and there),
# and does not get DC applied for extended periods of time (only 2 out of ~20 light-applied blocks).
# It does get light of lots of various intensities and varying illumination field sizes (see notes 20190527 - pdf file).

# The more I'm analyzing the data, the more it's clear that this neuron indeed has its epochs of being more leaky,
# and during these epochs fast-event waveform shapes are distorted to be rounder and wider (and amplitude grouping becomes less clear).

# finding good parameter settings for extracting depolarizing events:
# block_no = 3 #2 # 1 # 0
# segment_no = 0
# time_slice = [30, 80]
#
# light pulse duration goes as low as 1ms, so setting ttleffect_window to 12 (to account for ChR activation etc.)
# APs have very pronounced AHPs usually ~150ms, extending window a bit to make sure it gets measured
# decreasing lpfilter and hpfilter values to get cleaner event-detect trace
# increasing min_depolamp to 0.3 - by eye, the smallest clearly visible events are 0.5mV, below that amplitude we start to get noise, and below 0.3mV it's impossible to tell.
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     ttleffect_window=12,
#                                     min_depolamp=0.3,
#                                     ahp_width_window=200,
#                                     noisefilter_hpfreq=2000,
#                                     oscfilter_lpfreq=7,
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(ttleffect_window=12,
#                                     min_depolamp=0.3,
#                                     ahp_width_window=200,
#                                     noisefilter_hpfreq=2000,
#                                     oscfilter_lpfreq=7,)
# singleneuron_data.write_results()

# %% plots and analyses: labeling depolarizing events categories
# des_df = singleneuron_data.depolarizing_events

# 1. seeing light/puff-evoked things (mostly to be sure that they're not accidentally contaminating spont.events)
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# Responses to light are mostly clearly compound, and the recorded neuron is not the only one
# in the network being affected, as evidenced by there being some oscillations following stronger/larger light pulses.
# Still, the peaks and baselines picked up by the event-finding algorithm generally correspond quite well to where Yosi
# would point. Here and there it looks like a fast-event can be very easily isolated, either because it arrives just a
# bit later than all the other things going on in the response or because it looks like the response is only the
# fast-event - but then in the rest of the block there is usually no response at all to the light.
# However, by eye it does seem like fast-events are much more likely to occur within a second or two from the light
# than anywhere else in the 7s-long trace.

# 2. plotting events parameters to see where to start narrowing down on fast-events:
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events
#                             # & (des_df.baselinev >= -52)  # fastevents with baselinev lower than that got labeled as such already
#                             )

# There are MANY events, so let's first see histograms and scatters of parameters:
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('all as-yet unlabeled events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# No matter how many bins I plot with, there's a HUGE peak of events <1.5mV, and the next largest peak at ~1.8mV.
# also rise-time/amp scatters suggest a break there - looks like events <1.5mV have rise-time distributed rather evenly up till 4ms.
# Let's see parameter distributions for events <1.5mV only:
# probably_spikelets = (possibly_spontfastevents & (des_df.amplitude < 1.5))
# probably_spikelets_df = des_df[probably_spikelets]
# probably_spikelets_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# plt.suptitle('probably spikelets (not fast-events)')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_spikelets,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_spikelets,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_spikelets,
#                                                       )
#       alright, that all looks neatly in line with what we expect from spikelets
# and >1.5mV events only:
# probably_not_spikelets = (possibly_spontfastevents & (des_df.amplitude >= 1.5))
# des_df[probably_not_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# plt.suptitle('probably not spikelets')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_not_spikelets,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_not_spikelets,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=probably_not_spikelets,
#                                                       )
# my guess is most of these are fast-events, but the rise-time/amp scatter also suggests that in the
# smallest-amp group (~2mV) there's a lot of spikelets still
# let's see these events:
# singleneuron_data.plot_depolevents(probably_not_spikelets,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# OK, there's a lot else going on there as well but nonetheless it's very clear: there are 4 amplitude groups (3, 4, 6.5 and 9mV)
# and probably also a group of large-amp spikelets (2mV).
# The 'lot else' contains some double-events, and at more depolarized potentials (>-50mV) also weirder stuff that's
# gonna need a closer looking at.

# 3a. First, let's see only events occurring at baselinev < -70mV - looks like it was held there for just a little while,
# and there's a good chance there were only 'neat' events there.
# lowbaselinev_events = probably_not_spikelets & (des_df.baselinev < -70)
# singleneuron_data.plot_depolevents(lowbaselinev_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# the smallest amp-group - ~2mV - looks like spikelets (three of them riding another smaller depolarization).
# By amplitude the groups overlap, but it looks like we can get the spikelets by narrowing maxdvdt criteria:
# lowbaselinev_events_df = des_df[lowbaselinev_events]
# lowbaselinev_events_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='rise_time_20_80',
#                                                       lowbaselinev_events=lowbaselinev_events)
#
# probably_lowbaseline_spikelets = lowbaselinev_events & (des_df.maxdvdt < 0.14)
# singleneuron_data.plot_depolevents(probably_lowbaseline_spikelets,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
#
# probably_lowbaseline_fastevents = lowbaselinev_events & (des_df.maxdvdt >= 0.14)
# singleneuron_data.plot_depolevents(probably_lowbaseline_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# yea, those definitely look like fast-events - labeling them as such:
# singleneuron_data.depolarizing_events.loc[probably_lowbaseline_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3b. Next, let's see events with baselinev <-55mV:
# lowbaselinev_events = probably_not_spikelets & (des_df.baselinev >= -70) & (des_df.baselinev < -55)
# singleneuron_data.plot_depolevents(lowbaselinev_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# lowbaselinev_events_df = des_df[lowbaselinev_events]
# lowbaselinev_events_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='rise_time_20_80',
#                                                       lowbaselinev_events=lowbaselinev_events)
# this time, it looks like none of the events <2.5mV may be fast-events; but other measures may also be good criteria
# probably_lowbaseline_spikelets = lowbaselinev_events & (des_df.amplitude < 2.5)
# singleneuron_data.plot_depolevents(probably_lowbaseline_spikelets,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
#
# probably_lowbaseline_spikelets = lowbaselinev_events & (des_df.maxdvdt < 0.12)
# singleneuron_data.plot_depolevents(probably_lowbaseline_spikelets,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# this one's the winner - going by amplitude keeps one stray fast-event in the spikelet-group

# Now let's see whether we're left with only fast-events:
# probably_lowbaseline_fastevents = lowbaselinev_events & (des_df.maxdvdt >= 0.12)
# singleneuron_data.plot_depolevents(probably_lowbaseline_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# looks like that one 2mV event that was kept isn't exactly a fast-event after all - it stands out also in its dvdt/V-plot shape
# probably_lowbaseline_fastevents = lowbaselinev_events & (des_df.amplitude >= 2.5)
# singleneuron_data.plot_depolevents(probably_lowbaseline_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# looks like there's still some things in there that aren't exactly single fast-events; let's see the histograms
# probably_lowbaseline_fastevents_df = des_df[probably_lowbaseline_fastevents]
# probably_lowbaseline_fastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# looks like there's just a handful of events with rise-time > 0.75ms; let's see if filtering those
# will get rid of the outlier-looking lines in the dVdt/V plot:
# probably_lowbaseline_fastevents = probably_lowbaseline_fastevents & (des_df.rise_time_20_80 < 0.75)
# singleneuron_data.plot_depolevents(probably_lowbaseline_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# that looks like it's gonna be as neat as it's gonna get - any variation in dVdt/V plot shape
# looks to be coming from some of the events are riding a slow prepotenitial of up to ~1mV.
# labeling these events as fastevents:
# singleneuron_data.depolarizing_events.loc[probably_lowbaseline_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3c. Next, let's see events with baseline <-52mV:
# lowbaselinev_events = probably_not_spikelets & (des_df.baselinev >= -55) & (des_df.baselinev < -52)
# singleneuron_data.plot_depolevents(lowbaselinev_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# looks like there may be three compound events there with amp also larger than all the others, as well as a bunch of
# mess in the range <6mV (events that are clearly rounder and wider than fast-events)
# let's see the parameters:
# lowbaselinev_events_df = des_df[lowbaselinev_events]
# lowbaselinev_events_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='rise_time_20_80',
#                                                       lowbaselinev_events=lowbaselinev_events)
# looks like fast-events may be separable simply by width (break in the histogram at 3.5ms), let's see:
# probably_lowbaseline_fastevents = lowbaselinev_events & (des_df.width_50 <= 3.5)
# singleneuron_data.plot_depolevents(probably_lowbaseline_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# these are definitely all fast-events; labeling them as such:
# singleneuron_data.depolarizing_events.loc[probably_lowbaseline_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# next let's label the 4 largest events as compound_event:
# compound_events = lowbaselinev_events & (des_df.amplitude > 8)
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# now in the remaining events, it looks like those with maxdvdt < 0.11 are probably not fastevents:
# probably_lowbaseline_spikelets = lowbaselinev_events & (des_df.maxdvdt < 0.11)
# singleneuron_data.plot_depolevents(probably_lowbaseline_spikelets,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
#
# probably_lowbaseline_fastevents = lowbaselinev_events & (des_df.maxdvdt >= 0.11)
# singleneuron_data.plot_depolevents(probably_lowbaseline_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# yea that looks like a good split... The events with maxdvdt < 0.11 are all rather small (<2.5mV amp) and messy
# while the other events are larger (2 - 5.5mV amp) and a pretty neat normalized-waveform plot.
# The variance in the shape of the larger events is definitely getting bigger at this point, with events becoming
# a bit wider and rounder with increasing baselinev.
# It's possible that the group of small events contains 2 or 3 things that are in fact tiny fast-events (riding a pre-potential, amp ~1.5mV),
# but that's not a significant number of events relative to the grand total so I'm gonna ignore.
# labeling fast-events as such:
# singleneuron_data.depolarizing_events.loc[probably_lowbaseline_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3d. now let's move on to events with baselinev > -52mV, and get rid of some noise-stuff first: looks like events with
# baselinev > -41mV may be mostly just noise. Let's see:
# highbaselinev_events = probably_not_spikelets & (des_df.baselinev >= -41)
# singleneuron_data.plot_depolevents(highbaselinev_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# let's see the parameters:
# highbaselinev_events_df = des_df[highbaselinev_events]
# highbaselinev_events_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='rise_time_20_80',
#                                                       lowbaselinev_events=highbaselinev_events)
# Indeed, none of these things are actual events, just places where the neuron is temporarily very unhappy (very clear
# when plotting the events in the raw data traces). Marking them as noiseevents:
# singleneuron_data.depolarizing_events.loc[highbaselinev_events, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# In fact, seeing all events at baselinev > -41 (not just >1.5mV amp ones) shows that they're all just noise.
# Labeling them as such:
# highbaselinev_events = possibly_spontfastevents & (des_df.baselinev >= -41)
# singleneuron_data.depolarizing_events.loc[highbaselinev_events, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# Actually, let's see how far down we can go with baselinev and still get only noise-stuff - from looking at the
# raw data traces the boundary should be somewhere ~-44mV:
# highbaselinev_events = possibly_spontfastevents & (des_df.baselinev >= -43.5)
# singleneuron_data.plot_depolevents(highbaselinev_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# Indeed, nothing with baselinev in that range are actual events. Labeling them as noiseevent:
# singleneuron_data.depolarizing_events.loc[highbaselinev_events, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# 3e. Now in the events that we're left with, it looks like events with baselinev <-48mV (at least the bigger ones)
# may be all 'neat' fast-events; let's see:
# baselinerange_events = probably_not_spikelets & (des_df.baselinev < -48)
# singleneuron_data.plot_depolevents(baselinerange_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# let's see the parameters:
# baselinerange_events_df = des_df[baselinerange_events]
# baselinerange_events_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='rise_time_20_80',
#                                                       lowbaselinev_events=baselinerange_events)
# OK: it's pretty clear that there's groups, but also that the groups may be two different types of events...
# there's events with amp up to 6mV that definitely do not have the same normalized waveform as the handful
# of fast-events that are also there - they have a much rounder and wider shape.
# Here's the thing though: looking at where groups of events are in the raw data, it is evident that these
# 'rounder fast-events' are occurring there where the recording quality is deteriorating (especially towards the
# very end, in the last light file (0021) it is very clear that the place where the neuron depolarizes and becomes
# leaky is where these events start coming on.
# I'll find the few neat fast-events that were recorded in this baselinev range, and leave the rest to look at more
# closely and then decide what to do with.
# Looks like the groups should be separable by maxdvdt:
# baselinerange_otherevents = baselinerange_events & (des_df.maxdvdt <= 0.35)
# singleneuron_data.plot_depolevents(baselinerange_otherevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )

# probably_baselinerange_fastevents = baselinerange_events & (des_df.maxdvdt > 0.35)
# singleneuron_data.plot_depolevents(probably_baselinerange_fastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# definitely getting closer to grabbing only neat fast-events. The largest-amp event (12mV) is compound,
# labeling it as such:
# compound_event = probably_baselinerange_fastevents & (des_df.amplitude > 11)
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# the remaining events are fast-events - normalized waveform is practically identical (it kinda looks like there
# could be two groups (one just a tad slower than the other, so that the peak-alignment is off) but this can be
# explained by there being more than an hour of recording time between them.
# Labeling fast-events as such:
# singleneuron_data.depolarizing_events.loc[probably_baselinerange_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Now let's take the 'other events' - sure, they have a rounder shape than the neat fast-events, but aside from a few
# things that rise a bit slower than the rest and don't decay very nicely at all (i.e., are more like noise-events)
# these could all easily still be fast-events. Let's see if we get rid of the noise by excluding events with rise-time
# > 1.5ms (there's a clean break in the histogram there):
# possibly_noiseevents = (baselinerange_otherevents & (des_df.rise_time_20_80 > 1.5))
# singleneuron_data.plot_depolevents(possibly_noiseevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# indeed, these are all very noisy-looking things - even if they may be fast-events, they are very small (~2mV) and riding noise-wobbles that further distort their measures badly.
# possibly_deterioratedfastevents = (baselinerange_otherevents & (~possibly_noiseevents))
# singleneuron_data.plot_depolevents(possibly_deterioratedfastevents,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=12,
#                                    )
# indeed, the remaining events even normalize pretty nicely to be of very similar waveforms.
# Labeling events appropriately:
# singleneuron_data.depolarizing_events.loc[possibly_noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.depolarizing_events.loc[possibly_deterioratedfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3f. Now let's see all events with baselinev < -47mV:
# baselinerange_events = probably_not_spikelets & (des_df.baselinev < -47)
# they don't all look very neat, but by their parameter distributions these are all fast-events. Labeling as such:
# singleneuron_data.depolarizing_events.loc[baselinerange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3g. events with baselinev < -46mV:
# baselinerange_events = probably_not_spikelets & (des_df.baselinev < -46)
# again there is a bit of variability in the shape, but parameter ranges all look right on for fast-events so that's
# probably because of changing recording conditions. Labeling them:
# singleneuron_data.depolarizing_events.loc[baselinerange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3h. events with baselinev < -45mV:
# baselinerange_events = probably_not_spikelets & (des_df.baselinev < -45)
# some of these events are clearly compound, but they're proving to be very hard to separate from the rest by any
# measure for all amplitude groups, so splitting them out further:
# amplituderange_events = (baselinerange_events & (des_df.amplitude > 4))
# within these, the two with the longest rise-time are compound (pre-potential of ~1.5mV). Labeling them as such:
# compound_events = (amplituderange_events & (des_df.rise_time_20_80 > 1.1))
# fastevents = (amplituderange_events & (des_df.rise_time_20_80 <= 1.1))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# amplituderange_events = (baselinerange_events & (des_df.amplitude > 2))
# within these, the two with the widest width are clearly compound; also in the fast-events group there's one that looks
# kinda compound to me (it has a kina bent rising phase), but the dVdt-plot and the parameter distributions seem to
# disagree with me so keeping it in the fastevents group.
# compound_events = (amplituderange_events & (des_df.width_50 > 6))
# fastevents = (amplituderange_events & (des_df.width_50 <= 6))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# in the remaining events there are some clearly compound ones, and two of them just won't let me grab them by
# parameters... So going bit by bit:
# compound_events = (baselinerange_events & (des_df.rise_time_20_80 >= 1.2))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# compound_events = (baselinerange_events & (des_df.width_50 >= 5.5))
# one of these might be not exactly compound, but they're being too annoying and I don't care about one event here or
# there anymore so labeling them:
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# in the last remaining events there's still one that is clearly compound, yet I can't seem to grab it in any way...
# Been trying for too long already, giving up now. Labeling all remaining events as fast-events:
# singleneuron_data.depolarizing_events.loc[baselinerange_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3h. events with baselinev >= -45mV:
# baselinerange_events = probably_not_spikelets & (des_df.baselinev >= -45)
#
# singleneuron_data.plot_depolevents(baselinerange_events,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    # timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=12,
#                                    )
# des_df[baselinerange_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# There are a few compound events in there and one stray noise-thing. Going by amplitude-group to label them:
# baselinerange_events_ampgroup1 = (baselinerange_events & (des_df.amplitude > 4))
# singleneuron_data.plot_depolevents(baselinerange_events_ampgroup1,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    # timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=12,
#                                    )
# des_df[baselinerange_events_ampgroup1].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# honestly, it's a little hard to say which ones of these are compound and which aren't - they're all kinda noisy with
# peaks that look a little messed-up. But only the single largest event has a clear second wobble in the dVdt/V plot,
# so labeling that as compound-event and the rest as fast-events:
# compound_event = (baselinerange_events_ampgroup1 & (des_df.amplitude > 7.5))
# fast_events = (baselinerange_events_ampgroup1 & (des_df.amplitude < 7.5))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# The now remaining events all look like fast-events, except for the one noise-thing - maybe some have a tiny wobble in
# the dVdt but it's hard to say with the noise. Normalized they all look to have the same decay, except for the
# noise-thing which doesn't have a width-measurement. Labeling them:
# noiseevent = (baselinerange_events & (des_df.width_50.isna()))
# fast_events = (baselinerange_events & (~des_df.width_50.isna()))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 4. In the now remaining possibly_spontfastevents we're left with just a few large-amp ones, and a big group with amp~2mV
# 4a. first, let's see events with amp>2.8mV:
# events_largeamp = (possibly_spontfastevents & (des_df.amplitude > 2.8))
# singleneuron_data.plot_depolevents(events_largeamp,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    # timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=12,
#                                    )
# des_df[events_largeamp].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
# The two largest ones of these look compound, having a clear wobble in the dVdt/V plot. The other ones don't look all
# too clean either, but that's most likely due to recording conditions - cell goes through some bad noise but comes
# back and fires off these events. Labeling them:
# compoundevents = (possibly_spontfastevents & (des_df.amplitude > 8))
# fastevents = (possibly_spontfastevents & (des_df.amplitude > 2.8) & (des_df.amplitude < 8))
# singleneuron_data.depolarizing_events.loc[compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# 4b. in the now remaining possibly_spontfastevents, there's a break in amplitudes ~1.5mV and clearly a group of
# fast-events with amp~2mV and rise-time to match. Events with similar amplitude but longer rise-time are likely to be
# compound events. Going over them in baselinev groups, in order to see properly:
# events with baselinev<-60mV:
# out of these, three have a clear pre-potential of ~0.5mV and are easy to separate by rise-time; labeling these as
# compound events, the rest as fast-events:
# compoundevents = (events_underinvestigation & (des_df.rise_time_20_80 > 1.5))
# fast_events = (events_underinvestigation & (des_df.rise_time_20_80 < 1.5))
# singleneuron_data.depolarizing_events.loc[compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinev<-55mV:
# out of these, there are a few that have a ~0.5mV pre-potential; also in the rise-time histogram there is clearly
# a group, and then some outliers. There are a few more events whose decay seems by eye to be clearly affected by
# something, yet by parameters or from the dVdt/V-plot I could not capture these separately, so they'll all get labeled
# as fast-events.
# compoundevents = (events_underinvestigation & (des_df.rise_time_20_80 > 1.25))
# fast_events = (events_underinvestigation & (des_df.rise_time_20_80 < 1.25))
# singleneuron_data.depolarizing_events.loc[compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.depolarizing_events.loc[fast_events, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinev<-50mV:
# from looking at these plotted together it would seem that there is some variation there, with some events having a
# small pre-potential and others perhaps even being properly compound; however, things are noisy enough that they
# cannot be separated from 'simply noisy' events by any parameters. So labeling them all as fast-events:
# singleneuron_data.depolarizing_events.loc[events_underinvestigation, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()
# events with baselinev<-40mV (all remaining events):
# There are no more events with amp>1.5mV left, and also the histograms and scatters of the parameters corroborate the
# idea that there are no more fast-events to find.

# events_underinvestigation = (possibly_spontfastevents & (des_df.amplitude > 1.5) & (des_df.baselinev < -40))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plot_dvdt=True,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    # timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=12,
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)

# Looking at the events again more closely, there are some events in the smallest group (~2mV) that are in fact
# compound. A few stand out especially because they're also neat events). Labeling them as such:
# compoundevents = (fastevents & probably_neatevents
#                                     & (des_df.width_70 >= 3.85)
#                                     & (des_df.amplitude < 1.95))
# singleneuron_data.depolarizing_events.loc[compoundevents, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()
# there are some more also in the events not marked 'neat', but I can't seem to grab them easily by any parameter so
# leaving them be for now.
### -- this concludes finding fast-events for this neuron -- ###
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks('gapFree',
#                                      events_to_mark=(fastevents | compound_events),
#                                      segments_overlayed=False)
# this neuron's fast-events are very infrequent at first, becoming more frequent in the first 5 min. or so of recording
# and then decreasing in frequency again after about an hour of recording (neuron also stops firing APs at this point).
# Up to and including gapFree_0005 recording is very nice and stable (slight decrease in AP amp, goes to +50mV initially
# and to +40mV by the end of gapFree_0005). After that there are some drift-events, so I'll stick to the time before that.

# probably_neatevents = (des_df.file_origin.str.match(pat=('gapFree|light_0')))
# probably_neatevents = (probably_neatevents & ~(des_df.file_origin == 'gapFree_0006.abf'))

# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()



# %% plots for publication figures --  figure 1 draft 3.2
# !!note: smallest group may be a spikelet after all (~2mV amp)
# make the different amplitude groups in different colors
# sampling_frequency = singleneuron_data.blocks[1].channel_indexes[0].analogsignals[0].sampling_rate
# neatevents_50s_startidx = (906.5 * float(sampling_frequency))
# neatevents_50s_endidx = (956.5 * float(sampling_frequency))
# neatevents_50s = ((des_df.file_origin == 'gapFree_0004.abf')
#                   & (des_df.peakv_idx > neatevents_50s_startidx)
#                   & (des_df.peakv_idx < neatevents_50s_endidx))
# figure, axes = singleneuron_data.plot_rawdatablocks('gapFree_0004', events_to_mark=(fastevents & neatevents_50s))
# axes[0].set_xlim(906500, 956500)
# axes[0].set_ylim(-60, -40)
# axes[0].vlines(x=915375, ymin=-60, ymax=-40)
# axes[0].vlines(x=915575, ymin=-60, ymax=-40)
# axes[0].vlines(x=916750, ymin=-60, ymax=-40)
# axes[0].vlines(x=916950, ymin=-60, ymax=-40)
#
# singleneuron_data.plot_depolevents((fastevents & neatevents_50s),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plotwindow_inms=15,
#                                    plt_title=' neat fast-events'
#                                    )

# %% plots for publication figures -- figure1 draft1
# ## selecting events to plot
# # let's see the amplitude/baselinev scatter for fast-events, to choose a narrow baselinev range to plot for:
# singleneuron_data.scatter_depolarizingevents_measures('baselinev', 'amplitude',
#                                                       fast_events=fast_events)
# # looks like between -55.5 - -56.0mV all ampgroups are represented (except maybe one of barely 2mV, which is not that frequent anyway)
# # so let's plot these:
# baselinerange_events = ((des_df.baselinev > -56) & (des_df.baselinev < -55.5) & (~des_df.applied_ttlpulse))
# baselinerange_fastevents = (fast_events & baselinerange_events)
# baselinerange_spikelets = (probably_spikelets & baselinerange_events & (des_df.amplitude > 0.5))  #
#
# singleneuron_data.plot_depolevents(baselinerange_fastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=12,
#                                    prealignpoint_window_inms = 3,
#                                    plot_dvdt=True)
# singleneuron_data.plot_depolevents(baselinerange_spikelets,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=12,
#                                    prealignpoint_window_inms = 3,
#                                    plot_dvdt=True)
# ## plot comparing fast-events and spikelets:
# singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, baselinerange_spikelets,
#                                                    group_labels=['fast_events', 'spikelets'],
#                                                    plotwindow_inms=12,
#                                                    prealignpoint_window_inms = 3,
#                                                    plot_dvdt=True
#                                                    )
# ## plots of normalized waveforms - mostly fast-events, with just a few spikelets for comparison:
#     # that narrows it down well enough for me, can always remove more lines in illustrator
# # singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, baselinerange_spikelets,
# #                                                    group_labels=['fast_events', 'spikelet'],
# #                                                    plotwindow_inms=12,
# #                                                    prealignpoint_window_inms = 3,
# #                                                    plot_dvdt=True,
# #                                                    do_normalizing=True,
# #                                                    )
# # let's narrow down on the spikelets some so that they're not crowding the plot too much
# selected_spikelets = (baselinerange_spikelets & (((des_df.amplitude > 2.2) & (des_df.amplitude < 2.3))
#                                         | ((des_df.amplitude > 0.62) & (des_df.amplitude < 0.64)) ))
# singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, selected_spikelets,
#                                                    group_labels=['fast_events', 'spikelet'],
#                                                    plotwindow_inms=12,
#                                                    prealignpoint_window_inms = 3,
#                                                    plot_dvdt=True,
#                                                    do_normalizing=True,
#                                                    )
# # %%
# ## voltage dependence of the waveform shape
# # picking an amp-range based on amplitude/baselinev histogram
# # amprange_fastevents = (fast_events & (des_df.amplitude > 4.14) & (des_df.amplitude < 4.21))  # too messy, doesn't clearly show the effect we want to see
# amprange_fastevents = (fastevents & (des_df.amplitude > 5.8) & (des_df.amplitude < 5.9))
# singleneuron_data.plot_depolevents(amprange_fastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=15,
#                                    prealignpoint_window_inms = 3,
#                                    plot_dvdt=True)
#
# ## histograms of events parameters:  # just tinkering with nbins here to get good-looking distributions, should really write some code for doing that more properly
# # amplitude, baselinerange
# plt.figure()
# des_df.loc[baselinerange_spikelets, 'amplitude'].hist()
# des_df.loc[baselinerange_fastevents, 'amplitude'].hist(bins=30)
# plt.suptitle('amplitude, events within baselinerange')
# # amplitude, all
# plt.figure()
# des_df.loc[probably_spikelets, 'amplitude'].hist(bins=30)
# des_df.loc[fast_events, 'amplitude'].hist(bins=40)
# plt.suptitle('amplitude, all fast-events and spikelets')
# # rise-time, baselinerange
# plt.figure()
# des_df.loc[baselinerange_spikelets, 'rise_time_20_80'].hist(bins=100)
# des_df.loc[baselinerange_fastevents, 'rise_time_20_80'].hist(bins=1)
# plt.suptitle('rise-time (20-80%), events within baselinerange')
# # rise-time, all
# plt.figure()
# des_df.loc[probably_spikelets, 'rise_time_20_80'].hist(bins=100)
# des_df.loc[fast_events, 'rise_time_20_80'].hist(bins=10)
# plt.suptitle('rise_time_20_80, all fast-events and spikelets')
# # half-width, baselinerange
# plt.figure()
# des_df.loc[baselinerange_spikelets, 'width_50'].hist(bins=100)
# des_df.loc[baselinerange_fastevents, 'width_50'].hist(bins=3)
# plt.suptitle('half-width, events within baselinerange')
# # half-width, all
# plt.figure()
# des_df.loc[probably_spikelets, 'width_50'].hist(bins=100)
# des_df.loc[fast_events, 'width_50'].hist(bins=10)
# plt.suptitle('half-width, all fast-events and spikelets')
# # maxdvdt, baselinerange
# plt.figure()
# des_df.loc[baselinerange_spikelets, 'maxdvdt'].hist()
# des_df.loc[baselinerange_fastevents, 'maxdvdt'].hist(bins=40)
# plt.suptitle('maxdvdt, events within baselinerange')
# # maxdvdt, all
# plt.figure()
# des_df.loc[probably_spikelets, 'maxdvdt'].hist(bins=10)
# des_df.loc[fast_events, 'maxdvdt'].hist(bins=30)
# plt.suptitle('maxdvdt, all fast-events and spikelets')
# # %%
# ## scatters of events parameters:
# baselinerange_aps = (aps & baselinerange_events)
# # amplitude vs rise-time, baselinerange
# singleneuron_data.scatter_depoleventsgroups_overlayed('rise_time_20_80', 'amplitude',
#                                                       fast_events=baselinerange_fastevents,
#                                                       spikelets=baselinerange_spikelets,
#                                                       # aps=baselinerange_aps,
#                                                       plt_title='events within baselinerange')
# # amplitude vs rise-time, all
# singleneuron_data.scatter_depoleventsgroups_overlayed('rise_time_20_80', 'amplitude',
#                                                       fast_events=fast_events,
#                                                       spikelets=probably_spikelets,
#                                                       # aps=aps,
#                                                       plt_title='all spikelets and fast-events'
#                                                       )
#
# # amplitude vs half-width, baselinerange
# singleneuron_data.scatter_depoleventsgroups_overlayed('width_50', 'amplitude',
#                                                       fast_events=baselinerange_fastevents,
#                                                       spikelets=baselinerange_spikelets,
#                                                       # aps=baselinerange_aps,
#                                                       plt_title='events within baselinerange')
# # amplitude vs half-width, all
# singleneuron_data.scatter_depoleventsgroups_overlayed('width_50', 'amplitude',
#                                                       fast_events=fast_events,
#                                                       spikelets=probably_spikelets,
#                                                       # aps=aps,
#                                                       plt_title='all spikelets and fast-events')
#
# # amplitude vs maxdvdt, baselinerange
# singleneuron_data.scatter_depoleventsgroups_overlayed('maxdvdt', 'amplitude',
#                                                       fast_events=baselinerange_fastevents,
#                                                       spikelets=baselinerange_spikelets,
#                                                       # aps=baselinerange_aps,
#                                                       plt_title='events within baselinerange')
# # amplitude vs maxdvdt, all
# singleneuron_data.scatter_depoleventsgroups_overlayed('maxdvdt', 'amplitude',
#                                                       fast_events=fast_events,
#                                                       spikelets=probably_spikelets,
#                                                       # aps=aps,
#                                                       plt_title='all spikelets and fast-events')
# %% plots for publication figures -- MSdraft version3 (APs first), figure 1
# selecting ~5min. of recording to show events from, so as not to have too many traces in the plot
samplingrate = float(singleneuron_data.blocks[1].channel_indexes[0].analogsignals[0].sampling_rate)
selection_startidx = samplingrate * 350
selection_endidx = samplingrate * 650
selected_events = ((des_df.file_origin == 'gapFree_0004.abf')
                   & (des_df.peakv_idx > selection_startidx)
                   & (des_df.peakv_idx < selection_endidx)
                   )
aps_axis, aps_dvdt_axis = singleneuron_data.plot_depolevents((aps & selected_events
                                    ),
                                   colorby_measure='baselinev',
                                   # timealignto_measure='rt20_start_idx',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=4,
                                   plotwindow_inms=12,
                                   )

fastevents_axis, fastevents_dvdt_axis = singleneuron_data.plot_depolevents(
    (fastevents & selected_events & (des_df.amplitude > 3)
                                    ),
                                   colorby_measure='baselinev',
                                   # timealignto_measure='rt20_start_idx',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=4,
                                   plotwindow_inms=12,
                                   )

# saving the figures, then re-scaling axes:
aps_axis.set_xlim([0, 6])
aps_axis.set_ylim([-1, 12])
aps_dvdt_axis.set_ylim([-0.15, 0.8])
aps_dvdt_axis.set_xlim([-1, 12])

fastevents_axis.set_xlim([0, 6])
fastevents_axis.set_ylim([-1, 12])
fastevents_dvdt_axis.set_ylim([-0.15, 0.8])
fastevents_dvdt_axis.set_xlim([-1, 12])

# %%
# plotting light-evoked activity: first 10 traces of the nicest-looking file (and leaving out traces where fast response starts too late to see in zoomed-in view)
figure, axes = singleneuron_data.plot_rawdatatraces_ttlaligned('light_0003',
                                                skip_vtraces_idcs=[2, 4, 8,
                                                                   10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
# save figure, then re-scaling axes:
# axes[0].set_xlim([5, 11])
# axes[0].set_ylim([-1, 12])
# axes[1].set_ylim([-0.15, 0.8])
# axes[1].set_xlim([-1, 12])


