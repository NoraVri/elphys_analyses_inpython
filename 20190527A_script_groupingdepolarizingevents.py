# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190527A'
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
nbins = 150
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)


# all the kinds of interesting events detected in this neuron:
aps = des_df.event_label == 'actionpotential'
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section3-
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section3-
smallslowevents = des_df.event_label.isna()  # see plots and analyses section2,

# %% analyses summary plots:
# singleneuron_data.plot_depoleventsgroups_overlayed(aps, fast_events, compound_events, possibly_unlabeledspontfastevents, probably_spikelets,
#                                                    group_labels=['APs', 'fastevents', 'compound events', 'possibly fast-events', 'probably_spikelets'],
#                                                    do_baselining=True,
#                                                    # do_normalizing=True,
#                                                    plot_dvdt=True,
#                                                    )
# aps
des_df[aps].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
                         'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
plt.suptitle('aps')
singleneuron_data.plot_depolevents(aps, colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15,
                                   plt_title=' action potentials')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      aps=aps)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      aps=aps)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      aps=aps)

# fast-events
des_df[fastevents].hist(column=['rise_time_20_80', 'width_50', 'amplitude',
                                # 'baselinev', 'maxdvdt',
                                # 'approx_oscinstphase', 'approx_oscslope'
                                ],
                        bins=nbins)
plt.suptitle('fast-events')
singleneuron_data.plot_depolevents(fastevents, colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15,
                                   plt_title=' fast-events')
singleneuron_data.plot_depolevents(fastevents, colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15,
                                   plt_title=' fast-events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fastevents)

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
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      compound_events=compound_events)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      compound_events=compound_events)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      compound_events=compound_events)

# things that are probably spikelets
des_df[smallslowevents].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev', 'approx_oscinstphase', 'approx_oscslope'], bins=nbins)
plt.suptitle('small, slow events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      probably_spikelets=smallslowevents)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      probably_spikelets=smallslowevents)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      probably_spikelets=smallslowevents)
singleneuron_data.plot_depolevents((smallslowevents & (des_df.amplitude > 1)), colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=10,
                                   plt_title=' small slow events')

# %% plots for publication figures
bins=20
sampling_rate = int(singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate)
probably_neatevents = ((des_df.file_origin == 'gapFree_0004.abf')
                       & (des_df.peakv_idx > (550 * sampling_rate))
                       # & (des_df.peakv_idx < (850 * sampling_rate))  # a more or less random 5 minutes from within the trace really, it's all quite nice and stable
                       )

singleneuron_data.plot_rawdatablocks('gapFree_0004', events_to_mark=(fastevents & probably_neatevents))
singleneuron_data.plot_depolevents((fastevents & probably_neatevents),
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plotwindow_inms=14,
                                   plt_title=' neat fast-events'
                                   )
des_df[(fastevents & probably_neatevents)].hist(column=['rise_time_20_80', 'width_50', 'amplitude',
                                                        # 'baselinev', 'approx_oscinstphase', 'approx_oscslope', 'maxdvdt',
                                                        ],
                                                 bins=bins)
plt.suptitle('fast-events, neat ones only')
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
des_df = singleneuron_data.depolarizing_events

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
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events
                            & (des_df.baselinev >= -52)  # fastevents with baselinev lower than that got labeled as such already
                            )

# There are MANY events, so let's first see histograms and scatters of parameters:
possibly_spontfastevents_df = des_df[possibly_spontfastevents]
possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
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
probably_not_spikelets = (possibly_spontfastevents & (des_df.amplitude >= 1.5))
des_df[probably_not_spikelets].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
plt.suptitle('probably not spikelets')
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
baselinerange_events = probably_not_spikelets & (des_df.baselinev >= -45)

singleneuron_data.plot_depolevents(baselinerange_events,
                                   colorby_measure='baselinev',
                                   plot_dvdt=True,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   # timealignto_measure='rt20_start_idx',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=12,
                                   )
des_df[baselinerange_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)










# %% plots for publication figures -- figure1 draft1
## selecting events to plot
# let's see the amplitude/baselinev scatter for fast-events, to choose a narrow baselinev range to plot for:
singleneuron_data.scatter_depolarizingevents_measures('baselinev', 'amplitude',
                                                      fast_events=fast_events)
# looks like between -55.5 - -56.0mV all ampgroups are represented (except maybe one of barely 2mV, which is not that frequent anyway)
# so let's plot these:
baselinerange_events = ((des_df.baselinev > -56) & (des_df.baselinev < -55.5) & (~des_df.applied_ttlpulse))
baselinerange_fastevents = (fast_events & baselinerange_events)
baselinerange_spikelets = (probably_spikelets & baselinerange_events & (des_df.amplitude > 0.5))  #

singleneuron_data.plot_depolevents(baselinerange_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=12,
                                   prealignpoint_window_inms = 3,
                                   plot_dvdt=True)
singleneuron_data.plot_depolevents(baselinerange_spikelets,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=12,
                                   prealignpoint_window_inms = 3,
                                   plot_dvdt=True)
## plot comparing fast-events and spikelets:
singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, baselinerange_spikelets,
                                                   group_labels=['fast_events', 'spikelets'],
                                                   plotwindow_inms=12,
                                                   prealignpoint_window_inms = 3,
                                                   plot_dvdt=True
                                                   )
## plots of normalized waveforms - mostly fast-events, with just a few spikelets for comparison:
    # that narrows it down well enough for me, can always remove more lines in illustrator
# singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, baselinerange_spikelets,
#                                                    group_labels=['fast_events', 'spikelet'],
#                                                    plotwindow_inms=12,
#                                                    prealignpoint_window_inms = 3,
#                                                    plot_dvdt=True,
#                                                    do_normalizing=True,
#                                                    )
# let's narrow down on the spikelets some so that they're not crowding the plot too much
selected_spikelets = (baselinerange_spikelets & (((des_df.amplitude > 2.2) & (des_df.amplitude < 2.3))
                                        | ((des_df.amplitude > 0.62) & (des_df.amplitude < 0.64)) ))
singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, selected_spikelets,
                                                   group_labels=['fast_events', 'spikelet'],
                                                   plotwindow_inms=12,
                                                   prealignpoint_window_inms = 3,
                                                   plot_dvdt=True,
                                                   do_normalizing=True,
                                                   )
# %%
## voltage dependence of the waveform shape
# picking an amp-range based on amplitude/baselinev histogram
# amprange_fastevents = (fast_events & (des_df.amplitude > 4.14) & (des_df.amplitude < 4.21))  # too messy, doesn't clearly show the effect we want to see
amprange_fastevents = (fastevents & (des_df.amplitude > 5.8) & (des_df.amplitude < 5.9))
singleneuron_data.plot_depolevents(amprange_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=15,
                                   prealignpoint_window_inms = 3,
                                   plot_dvdt=True)

## histograms of events parameters:  # just tinkering with nbins here to get good-looking distributions, should really write some code for doing that more properly
# amplitude, baselinerange
plt.figure()
des_df.loc[baselinerange_spikelets, 'amplitude'].hist()
des_df.loc[baselinerange_fastevents, 'amplitude'].hist(bins=30)
plt.suptitle('amplitude, events within baselinerange')
# amplitude, all
plt.figure()
des_df.loc[probably_spikelets, 'amplitude'].hist(bins=30)
des_df.loc[fast_events, 'amplitude'].hist(bins=40)
plt.suptitle('amplitude, all fast-events and spikelets')
# rise-time, baselinerange
plt.figure()
des_df.loc[baselinerange_spikelets, 'rise_time_20_80'].hist(bins=100)
des_df.loc[baselinerange_fastevents, 'rise_time_20_80'].hist(bins=1)
plt.suptitle('rise-time (20-80%), events within baselinerange')
# rise-time, all
plt.figure()
des_df.loc[probably_spikelets, 'rise_time_20_80'].hist(bins=100)
des_df.loc[fast_events, 'rise_time_20_80'].hist(bins=10)
plt.suptitle('rise_time_20_80, all fast-events and spikelets')
# half-width, baselinerange
plt.figure()
des_df.loc[baselinerange_spikelets, 'width_50'].hist(bins=100)
des_df.loc[baselinerange_fastevents, 'width_50'].hist(bins=3)
plt.suptitle('half-width, events within baselinerange')
# half-width, all
plt.figure()
des_df.loc[probably_spikelets, 'width_50'].hist(bins=100)
des_df.loc[fast_events, 'width_50'].hist(bins=10)
plt.suptitle('half-width, all fast-events and spikelets')
# maxdvdt, baselinerange
plt.figure()
des_df.loc[baselinerange_spikelets, 'maxdvdt'].hist()
des_df.loc[baselinerange_fastevents, 'maxdvdt'].hist(bins=40)
plt.suptitle('maxdvdt, events within baselinerange')
# maxdvdt, all
plt.figure()
des_df.loc[probably_spikelets, 'maxdvdt'].hist(bins=10)
des_df.loc[fast_events, 'maxdvdt'].hist(bins=30)
plt.suptitle('maxdvdt, all fast-events and spikelets')
# %%
## scatters of events parameters:
baselinerange_aps = (aps & baselinerange_events)
# amplitude vs rise-time, baselinerange
singleneuron_data.scatter_depoleventsgroups_overlayed('rise_time_20_80', 'amplitude',
                                                      fast_events=baselinerange_fastevents,
                                                      spikelets=baselinerange_spikelets,
                                                      # aps=baselinerange_aps,
                                                      plt_title='events within baselinerange')
# amplitude vs rise-time, all
singleneuron_data.scatter_depoleventsgroups_overlayed('rise_time_20_80', 'amplitude',
                                                      fast_events=fast_events,
                                                      spikelets=probably_spikelets,
                                                      # aps=aps,
                                                      plt_title='all spikelets and fast-events'
                                                      )

# amplitude vs half-width, baselinerange
singleneuron_data.scatter_depoleventsgroups_overlayed('width_50', 'amplitude',
                                                      fast_events=baselinerange_fastevents,
                                                      spikelets=baselinerange_spikelets,
                                                      # aps=baselinerange_aps,
                                                      plt_title='events within baselinerange')
# amplitude vs half-width, all
singleneuron_data.scatter_depoleventsgroups_overlayed('width_50', 'amplitude',
                                                      fast_events=fast_events,
                                                      spikelets=probably_spikelets,
                                                      # aps=aps,
                                                      plt_title='all spikelets and fast-events')

# amplitude vs maxdvdt, baselinerange
singleneuron_data.scatter_depoleventsgroups_overlayed('maxdvdt', 'amplitude',
                                                      fast_events=baselinerange_fastevents,
                                                      spikelets=baselinerange_spikelets,
                                                      # aps=baselinerange_aps,
                                                      plt_title='events within baselinerange')
# amplitude vs maxdvdt, all
singleneuron_data.scatter_depoleventsgroups_overlayed('maxdvdt', 'amplitude',
                                                      fast_events=fast_events,
                                                      spikelets=probably_spikelets,
                                                      # aps=aps,
                                                      plt_title='all spikelets and fast-events')

