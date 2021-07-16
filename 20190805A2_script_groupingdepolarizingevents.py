# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190805A2'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# oscillating neuron


des_df = singleneuron_data.depolarizing_events
nbins = 250

aps = des_df.event_label == 'actionpotential'
fast_events = des_df.event_label == 'fastevent'
# comound_events = des_df.event_label == 'compound_event'
huge_events = des_df.event_label == 'hugeevent'
# possibly_unlabeledspontfastevents = ((~des_df.applied_ttlpulse)
#                                      & des_df.event_label.isna()
#                                      & (des_df.amplitude > 3)
#                                      )
probably_spikelets = ((~des_df.applied_ttlpulse) & des_df.event_label.isna()
                      & (des_df.amplitude > 0.2) & (des_df.amplitude < 3))
# %% summary plots:
singleneuron_data.plot_depolevents(aps,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True)

singleneuron_data.plot_depolevents(huge_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True)

# singleneuron_data.plot_depolevents(possibly_unlabeledspontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )

singleneuron_data.plot_depoleventsgroups_overlayed(aps, fast_events, # huge_events,
                                                   group_labels=['APs', 'fastevents'],  # 'other huge events'],
                                                   do_baselining=True,
                                                   # do_normalizing=True,
                                                   plot_dvdt=True,
                                                   )

fast_events_df = des_df[fast_events]
fast_events_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'], bins=nbins)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=15)
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)

# %% plots for publication figures
## selecting events to plot
# let's see the amplitude/baselinev scatter for fast-events, to choose a narrow baselinev range to plot for:
singleneuron_data.scatter_depolarizingevents_measures('baselinev', 'amplitude',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('baselinev', 'ed_amplitude',
                                                      fast_events=fast_events)
# there's only one range where fast-events of all amplitudes seem to be represented:
baselinerange_events = ((des_df.baselinev > -53) & (des_df.baselinev < -51) & (~des_df.applied_ttlpulse))
baselinerange_fastevents = (fast_events & baselinerange_events)
baselinerange_spikelets = (probably_spikelets & baselinerange_events & (des_df.amplitude > 1))

singleneuron_data.plot_depolevents(baselinerange_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=15,
                                   prealignpoint_window_inms = 3,
                                   plot_dvdt=True)
singleneuron_data.plot_depolevents(baselinerange_spikelets,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=25,
                                   prealignpoint_window_inms = 10,
                                   plot_dvdt=True)
# that's waaay many spikelets, most of them not quite recognizable as such...
# and we're gonna need to see all these events with the oscillation subtracted, too.
singleneuron_data.plot_depolevents(baselinerange_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=15,
                                   prealignpoint_window_inms = 3,
                                   get_measures_type='ed',
                                   plot_dvdt=True)
singleneuron_data.plot_depolevents(baselinerange_spikelets,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=15,
                                   prealignpoint_window_inms = 3,
                                   get_measures_type='ed',
                                   plot_dvdt=True)
## plot comparing fast-events and spikelets:
# selecting fewer spikelets to display
selected_spikelets = (baselinerange_spikelets & (((des_df.amplitude > 1.2) & (des_df.amplitude < 1.3))
                                        | ((des_df.amplitude > 0.62) & (des_df.amplitude < 0.64)) ))
singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, selected_spikelets,
                                                   group_labels=['fast_events', 'spikelets'],
                                                   plotwindow_inms=15,
                                                   prealignpoint_window_inms = 3,
                                                   plot_dvdt=True,
                                                   get_measures_type='ed',
                                                   )
singleneuron_data.plot_depoleventsgroups_overlayed(baselinerange_fastevents, selected_spikelets,
                                                   group_labels=['fast_events', 'spikelets'],
                                                   plotwindow_inms=15,
                                                   prealignpoint_window_inms = 3,
                                                   plot_dvdt=True,
                                                   do_normalizing=True,
                                                   get_measures_type='ed',
                                                   )

## voltage dependence of the waveform shape
# picking an amp-range based on amplitude/baselinev histogram
amprange_fastevents = (fast_events & (des_df.ed_amplitude > 3.1) & (des_df.ed_amplitude < 3.4))  # there's one trace in there that basically doesn't decay, will take it out in illustrator
singleneuron_data.plot_depolevents(amprange_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=15,
                                   prealignpoint_window_inms = 3,
                                   plot_dvdt=True,
                                   get_measures_type='ed'
                                   )
# %%
## histograms of events parameters:  # just tinkering with nbins here to get good-looking distributions, should really write some code for doing that more properly
# amplitude, baselinerange, raw parameters
plt.figure()
# des_df.loc[baselinerange_spikelets, 'amplitude'].hist()
des_df.loc[baselinerange_fastevents, 'amplitude'].hist(bins=40)
plt.suptitle('amplitude, events within baselinerange')
# amplitude, all, raw parameters
plt.figure()
# des_df.loc[probably_spikelets, 'amplitude'].hist(bins=30)
des_df.loc[fast_events, 'amplitude'].hist(bins=80)
plt.suptitle('amplitude, all fast-events and spikelets')
# amplitude, baselinerange, event-detect-trace parameters
plt.figure()
# des_df.loc[baselinerange_spikelets, 'ed_amplitude'].hist()
des_df.loc[baselinerange_fastevents, 'ed_amplitude'].hist(bins=60)
plt.suptitle('ed_amplitude, events within baselinerange')
# amplitude, all, event-detect-trace parameters
plt.figure()
# des_df.loc[probably_spikelets, 'ed_amplitude'].hist(bins=10)
des_df.loc[fast_events, 'ed_amplitude'].hist(bins=40)
plt.suptitle('ed_amplitude, all fast-events and spikelets')
# %%
# width_50, baselinerange, raw parameters
plt.figure()
# des_df.loc[baselinerange_spikelets, 'width_50'].hist()
des_df.loc[baselinerange_fastevents, 'width_50'].hist(bins=40)
plt.suptitle('width_50, events within baselinerange')
# amplitude, all, raw parameters
plt.figure()
# des_df.loc[probably_spikelets, 'width_50'].hist(bins=30)
des_df.loc[fast_events, 'width_50'].hist(bins=80)
plt.suptitle('width_50, all fast-events and spikelets')
# amplitude, baselinerange, event-detect-trace parameters
plt.figure()
# des_df.loc[baselinerange_spikelets, 'ed_half_width'].hist()
des_df.loc[baselinerange_fastevents, 'ed_half_width'].hist(bins=60)
plt.suptitle('ed_half_width, events within baselinerange')
# amplitude, all, event-detect-trace parameters
plt.figure()
# des_df.loc[probably_spikelets, 'ed_half_width'].hist(bins=10)
des_df.loc[fast_events, 'ed_half_width'].hist(bins=40)
plt.suptitle('ed_half_width, all fast-events and spikelets')


# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# oscillations initially ~2mV amp, but growing reaching ~20mV eventually and going back and forth between
# small and large amp from time to time. Frequency is a pretty steady 8Hz, going wacky here and there.

# The result of extracting with default settings looks honestly really good - spikelets so tiny that Yosi would argue they're not even there
# get picked up from among the 20mV oscillations in recordings with blocker applied.
# However, in recordings with fast-events the 20Hz lp-filtered trace is affected by these a lot, and I'd like the
# subtracted oscillations trace to be neater so lowering that value. It's still not perfect - the larger the event
# the more the osctrace 'wobbles' there because of it. Yet phase extraction looks really good (especially gapFree 0).
# Now, while I'm quite sure that most of the tiny stuff that gets picked up do in fact correspond to spikelets,
# they are VERY hard to spot (whether in the raw data or the ed-trace) at amps below 0.3mV in most places because
# oscillations are so much bigger. So, increasing min_depolamp a bit.
# block_no = 0 # 0
# segment_no = 0
# time_slice = [300, 350] # [190, 240]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                     min_depolamp=0.2,
#                                     oscfilter_lpfreq=15,
# )


# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.2,
#                                                      oscfilter_lpfreq=15)
# singleneuron_data.write_results()


# %% finding fast-events
des_df = singleneuron_data.depolarizing_events

# 2. seeing that events got picked up nicely
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# I see one quite sizeable spikelet (~0.5mV; recurring quite regularly) that it seems has too slow rise-time to have
# gotten picked up by the algorithm; but given the sheer amount of spikelets that did get picked up I think it's insignificant.
# There's quite a lot of variability in AP amp, and some did not reach 0mV and did not get labeled as APs automatically.

# plotting events parameters:
# possibly_spontfastevents_df = des_df[possibly_spontfastevents]
# possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
#                                         'ed_maxdvdt', 'ed_rise_time_20_80', 'ed_half_width', 'ed_amplitude'],
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
# 100 bins don't cut it for seeing groups because parameters are distributed rather widely in the population of events;
# needed 200 - 400 initially to see the distributions well.
# There's definitely groupings in the amp and maxdvdt histograms, the group of smallest events (up to ~2mV or so)
# is HUGE. The split between spikelets and possible fast-events actually looks cleaner in maxdvdt, where the
# huge peak at low values has a quick dropoff to 0.075 - 0.1 or so.

# The scatters clearly show a handful of events with pretty quick rise-time and very large amp (35 - 50mV); I think
# these are probably APs that got mislabeled. Let's see them:
# probably_aps = (possibly_spontfastevents & (des_df.amplitude > 35))
# singleneuron_data.plot_depolevents(probably_aps,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    )
# Some of these look like APs with a low-amp Na-component: multiple peaks (as though riding a shoulder), and a pronounced AHP.
# Some of these just look like fast-events though, but huge ones (40-50mV amp); these occur only at the more hyperpolarized baselinev.
# There's a clear split in the max dvdt, let's see these two groups:
# singleneuron_data.plot_depolevents((probably_aps & (des_df.maxdvdt > 3)),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_depolevents((probably_aps & (des_df.maxdvdt < 3)),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    )
# I'm starting to think that these are simply huge events, most of them compound, with any difference in their
# decay shape/AHP arising from the ongoing oscillations...
# First of all, let's see actual APs that did get labeled as such, to compare to:
# aps = des_df.event_label == 'actionpotential'
# singleneuron_data.plot_depolevents(aps,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', events_to_mark=aps)
# OK, these are all definitely APs (also the one that happens at very depolarized baselinev - it's from an IV run).
# Indeed, spike amp is deteriorating continuously throughout recordings, but it seems that APs generally drive v to
# well below baseline on the AHP, so perhaps we can tell by that.
# So let's see these other huge events in the raw data:
# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', events_to_mark=probably_aps)
# I'm still not sure what to call them. Events with multiple peaks generally have a pretty pronounced AHP, despite
# no sign of a proper AP shoulder, yet single events without much of an AHP sometimes seem to have a bit of a shoulder.
# I give up, labeling these as 'hugeevents', adding them to summary plots and moving on with it:
# singleneuron_data.depolarizing_events.loc[probably_aps, 'event_label'] = 'hugeevent'
# singleneuron_data.write_results()

#
# Let's see parameter distributions split by maxdvdt, to see if there's any indication of fast-events being
# among events with the smallest maxdvdt values:
# events with maxdvdt < 0.08: (first peak in the maxdvdt histogram)
# probably_spikelets = (possibly_spontfastevents & (des_df.maxdvdt <= 0.08))
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
#       alright, that just looks in line with there being lots of spikelets (and loads of them being tiny).

# events with maxdvdt > 0.08:
maybe_not_spikelets = (possibly_spontfastevents & (des_df.maxdvdt > 0.08))
# maybe_not_spikelets_df = des_df[maybe_not_spikelets]
# maybe_not_spikelets_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
#                                         'ed_maxdvdt', 'ed_rise_time_20_80', 'ed_half_width', 'ed_amplitude'], bins=nbins)
# plt.suptitle('maybe not spikelets')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=maybe_not_spikelets,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=maybe_not_spikelets,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=maybe_not_spikelets,
#                                                       )
# The first thing that jumps out here are the handful of events with baselinev ~-10mV, let's see what's up with those:
# singleneuron_data.plot_depolevents((probably_not_spikelets & (des_df.baselinev > -20)),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    display_measures=True
#                                    )
# Those are all the same kind of double-event that got categorized as hugeevents before, except in these cases
# the second peak got picked up as event. Since they're the same kind of event that I didn't really know what
# to do with before, I'm gonna label these as hugeevents, too, for consistency's sake:
# singleneuron_data.depolarizing_events.loc[(probably_not_spikelets & (des_df.baselinev > -20)), 'event_label'] = 'hugeevent'
# singleneuron_data.write_results()

# Now for the remaining events:
# There's a clear divide in the risetime/amp scatter: there's a group of events with amp>3mV and rise_time_20_80 < 1,
# and the rest. Let's see the events split out like this:
possibly_fastevents = (maybe_not_spikelets & (des_df.amplitude > 3) & (des_df.rise_time_20_80 < 1))
possibly_fastevents_df = des_df[possibly_fastevents]
possibly_fastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
                                        'ed_maxdvdt', 'ed_rise_time_20_80', 'ed_half_width', 'ed_amplitude'], bins=nbins)
plt.suptitle('possibly fast-events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_fastevents=possibly_fastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_fastevents=possibly_fastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
                                                      cmeasure='baselinev',
                                                      possibly_fastevents=possibly_fastevents,
                                                      )
singleneuron_data.plot_depolevents(possibly_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plotwindow_inms=150,
                                   prealignpoint_window_inms=50,
                                   plt_title='possibly fast-events')
singleneuron_data.plot_depolevents(possibly_fastevents,
                                   get_measures_type='ed',
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plotwindow_inms=150,
                                   prealignpoint_window_inms=50,
                                   plot_dvdt=True,
                                   plt_title='possibly fast-events, osc subtracted')
# indeed, these all look like they should be fast-events.

# probably_not_fastevents = (probably_not_spikelets & (~possibly_fastevents))
# probably_not_fastevents_df = des_df[probably_not_fastevents]
# probably_not_fastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev',
#                                         'ed_maxdvdt', 'ed_rise_time_20_80', 'ed_half_width', 'ed_amplitude'], bins=nbins)
# plt.suptitle('probably not fast-events')
# singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       probably_not_fastevents=probably_not_fastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       probably_not_fastevents=probably_not_fastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_70',
#                                                       cmeasure='baselinev',
#                                                       probably_not_fastevents=probably_not_fastevents,
#                                                       )
# singleneuron_data.plot_depolevents(probably_not_fastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=10,
#                                    plt_title='probably not fast-events')
# singleneuron_data.plot_depolevents(probably_not_fastevents,
#                                    get_measures_type='ed',
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=10,
#                                    plot_dvdt=True,
#                                    plt_title='probably not fast-events, osc subtracted')
# here it seems that we're dealing with noisevents and non-events with VERY small amp, and a group of
# spikelets of ~2mV amp. But just to be sure that they're indeed spikelets, let's clean up and see:

# First, let's see what 'events' with ed_amp < 0.5 are (clear divide there in the amp histogram):
# probably_noiseevents = (probably_not_fastevents & (des_df.ed_amplitude < 0.6))
# singleneuron_data.plot_depolevents(probably_noiseevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plot_dvdt=True,
#                                    plotwindow_inms=10,
#                                    plt_title='probably not fast-events')
# singleneuron_data.plot_depolevents(probably_noiseevents,
#                                    get_measures_type='ed',
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    plotwindow_inms=10,
#                                    plot_dvdt=True,
#                                    plt_title='probably not fast-events, osc subtracted')
# indeed, these 'events' are all preceded by this weird fast negative noise that's in my recordings sometimes.
# Labeling them as noiseevents:
# singleneuron_data.depolarizing_events.loc[probably_noiseevents, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# As for the remaining events (amp ~0.5 - 2.5 mV), I cannot say for sure that there are no fast-events in there at all,
# but they're definitely not easy to pick out from among the events or by the parameter distributions.
# So, I will keep working with just the events > 3mV, as identified before; now that I'm convinced that I won't find
# any more, let's label them:
# singleneuron_data.depolarizing_events.loc[possibly_fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# %% splitting fast-events out by conditions: baselinev, oscphase, maxdvdt
# first: see for which events oscphase was nicely extracted
# singleneuron_data.plot_rawdatablocks(segments_overlayed=False, events_to_mark=fast_events)
# the overwhelming majority of them are in gapFree_0001, which is a nice long trace with mostly no pulses applied.
# oscillations are continuously ongoing, ~2mV amp initially (-48 - -50) and growing to ~8mV (peaks still at ~-48mV)
# time_slice = [700, 750] # [100, 150]  #
# singleneuron_data.plot_eventdetecttraces_forsegment(0 ,0, time_slice=time_slice)  # plotting this for the full 900s-or-so trace takes quite a while
# that looks really neat, with APs clearly causing small disruptions to phase progression but otherwise it's looking as smooth as it can
# so let's say all events from gapFree_0001 are 'neatevents', and see what they're up to relative to oscs.
neatevents = (fast_events & (des_df.file_origin == 'gapFree_0001.abf'))
neatevents_df = des_df[neatevents]
nbins = 100  # there's ~150 events altogether
neatevents_df.hist(column=['maxdvdt',
                           'rise_time_20_80',
                           'width_50',
                           'amplitude',
                           'baselinev',
                           'approx_oscslope',
                           'approx_oscinstphase',
                           'ed_maxdvdt', 'ed_rise_time_20_80', 'ed_half_width', 'ed_amplitude',], bins=nbins)
plt.suptitle('fast-events')

# now let's see events by criteria:
nbins = 50
# baselinev: towards the peak (>-48) or towards the bottom (<-52) of oscs
lowbaseline_events = (neatevents & (des_df.baselinev < -52))
highbaseline_events = (neatevents & (des_df.baselinev > -48))
des_df[lowbaseline_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',                           'baselinev',
                           'approx_oscslope',
                           'approx_oscinstphase',
                           'ed_maxdvdt', 'ed_rise_time_20_80', 'ed_half_width', 'ed_amplitude'], bins=nbins)
plt.suptitle('events with baselinev < -52')
singleneuron_data.plot_depolevents(lowbaseline_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='baselinev < -52'
                                   )

des_df[highbaseline_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events with baselinev > -48')
singleneuron_data.plot_depolevents(highbaseline_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='baselinev > -48',
                                   )

# oscphase: just before the peak (-1 - 0) vs just after the peak (0 - 1)
prepreak_events = (neatevents & (des_df.approx_oscinstphase > -1) & (des_df.approx_oscinstphase < 0))
des_df[prepreak_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events just before osc peak')
singleneuron_data.plot_depolevents(prepreak_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='events just before osc peak'
                                   )

postpeak_events = (neatevents & (des_df.approx_oscinstphase > 0) & (des_df.approx_oscinstphase < 1))
des_df[postpeak_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events just after osc peak')
singleneuron_data.plot_depolevents(postpeak_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='events just after osc peak'
                                   )

# oscphase: just before the trough (> 2.14) vs just after the trough (< -2.14)
pretrough_events = (neatevents & (des_df.approx_oscinstphase > 2.14))
des_df[pretrough_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events just before osc trough')
singleneuron_data.plot_depolevents(pretrough_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='events just before osc trough'
                                   )

posttrough_events = (neatevents & (des_df.approx_oscinstphase < -2.14))
des_df[posttrough_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events just after osc trough')
singleneuron_data.plot_depolevents(posttrough_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='events just after osc trough'
                                   )
# %%
# oscslope: upslope vs downslope
upslope_events = (neatevents & (des_df.approx_oscslope > 0))
des_df[upslope_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events on osc upslope')
singleneuron_data.plot_depolevents(upslope_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='events on osc upslope'
                                   )

downslope_events = (neatevents & (des_df.approx_oscslope < 0))
des_df[downslope_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',], bins=nbins)
plt.suptitle('events on osc downslope')
singleneuron_data.plot_depolevents(downslope_events,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   plot_dvdt=True,
                                   plt_title='events on osc downslope'
                                   )


# by maxdvdt value (should give the separate amplitude groups)




# also: see if those hugeevents could be fastevents, too













