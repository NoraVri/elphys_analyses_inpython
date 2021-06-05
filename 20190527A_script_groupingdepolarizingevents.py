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

# summary plots:
# all the kinds of interesting events detected in this neuron:
# aps = des_df.event_label == 'actionpotential'
# comound_events = des_df.event_label == 'compound_event'
# possibly_spontfastevents = ((~des_df.applied_ttlpulse) & des_df.event_label.isna() & (des_df.amplitude > 3))
#
# singleneuron_data.plot_depoleventsgroups_overlayed(aps, comound_events, possibly_spontfastevents,
#                                                    group_labels=['APs', 'compound events', 'possibly fast-events'],
#                                                    do_baselining=True,
#                                                    do_normalizing=True,
#                                                    plot_dvdt=True,
#                                                    )
#
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=2,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )

# fast_events = des_df.event_label == 'fastevent'
# fast_events_df = des_df[fast_events]
# fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
# singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)
# singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
#                                                       fast_events=fast_events)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# This neuron's got LOADS of events, by eye starting at ~2mV but also lots of big, very clear ones.
# Neuron is mostly holding steady throughout recordings (though some evidence of electrode drift here and there),
# and does not get DC applied for extended periods of time (only 2 out of ~20 light-applied blocks).
# It does get light of lots of various intensities and varying illumination field sizes (see notes 20190527 - pdf file).
#
# light pulse duration goes as low as 1ms, so setting ttleffect_window to 10 (to account for ChR activation etc.)
# setting min_depolamp to 2 for starters
# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=10)
# singleneuron_data.write_results()

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# If evoked events didn't get picked up it's because they are <2mV; honestly, the algorithm did a pretty amazing
# job at picking up events. Responses to light are mostly clearly compound, and the recorded neuron is not the only one
# in the network being affected, as evidenced by there being some oscillations following stronger/larger light pulses.
# Still, the peaks and baselines picked up by the event-finding algorithm generally correspond quite well to where Yosi
# would point. Here and there it looks like a fast-event can be very easily isolated, either because it arrives just a
# bit later than all the other things going on in the response or because it looks like the response is only the
# fast-event - but then in the rest of the block there is usually no response at all to the light.
# However, by eye it does seem like fast-events are much more likely to occur within a second or two from the light
# than anywhere else in the 7s-long trace.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# By eye it is clear that all events >2mV got picked up, and that these should be mostly fast-events.
# There is a spikelet of ~2mV that occasionally gets picked up (very recognizable for having a pronounced AHP),
# and I'd say it's possible that there are also fast-events among the ones with amp <2mV but they will definitely
# be mostly spikelets (and there are MANY of those).

# Let's see the amplitude and rise-time and width of all events in histograms and scatters:
# First impressions from the histograms: there must be a few outliers, because both in rise-time and width there are
# just a handful of events that are much longer than the rest.
# From the scatters it seems pretty clear that there should be at least three types of events:
# spikelets with amps up to ~2.5mV; fast-events with amp up to at least 10mV and rise-time 20-80 ~0.5ms; and
# another fast-event with amp ~6mV and rise ~1ms. The last two groups separate a bit better by rise 20-80 than 10-90,
# but may be somewhat overlapping in either case. Interestingly, the other fast-event seems to occur at much more
# narrow baselinev (-60 - -50) than fast-events (which occur anywhere between -80 - -40).
# Finally, there's a handful of outliers, some with pretty large amp (up to 20mV), mostly with large rise-time.

# Now let's see some events, and their amplitude and rise-time to narrow down from there:
# In the rise_time_20_80 histogram, there is a very steep drop at 1.2ms (from >100 to 10 events or less counted in
# all following bins). Let's start by seeing all events with rise_time_20_80 >= 1.2 to see what they might be:
# probably_notfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 >= 1.2))
# Things with amp<3mV look like they are of no interest to us: mostly very spikelet-shaped things and too many events
# with too much noise to tell anything apart. Let's see events with larger amplitude only:
# probably_notfastevents = (possibly_spontfastevents
#                           & (des_df.rise_time_20_80 >= 1.2)
#                           & (des_df.amplitude > 3))
# singleneuron_data.plot_depolevents(probably_notfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    prealignpoint_window_inms=50,
#                                    plotwindow_inms=250,
#                                    )
# One event is clearly a noise-thing, the single one occurring at the most depolarized potential (baselinev > -40).
# Labeling it as such:
# noiseevent = (probably_notfastevents & (des_df.baselinev > -41))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# In what we're left with now, the group of events with amp >10mV are clearly compound events.
# The other events look like they could be the other kind of fast-event, with just a single, pretty fast rising phase:
# singleneuron_data.plot_depolevents(probably_notfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )
# There can be no doubt from the dvdt-plot, the larger events are compound events with double rise.
# Labeling them as such:
# compound_events = (probably_notfastevents & (des_df.amplitude > 10))
# singleneuron_data.depolarizing_events.loc[compound_events, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# Now let's return to the parameter distributions of all events, sticking to the ones >3mV to escape
# multitudes of spikelets (there are plenty larger events to start with):
possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 3))
# The single very largest thing (amp almost 20mV) is clearly some noise-thing, labeling it as such:
# noiseevent = (possibly_spontfastevents & (des_df.amplitude > 18))
# singleneuron_data.depolarizing_events.loc[noiseevent, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

possibly_spontfastevents_df = des_df[possibly_spontfastevents]
nbins = 20
possibly_spontfastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_70',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# Let's see these events a bit more up-close:
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )

#Let's split them out by baselinev to get some more clarity:
# possibly_spontfastevents_lowbaseline = (possibly_spontfastevents & (des_df.baselinev <= -60))
# possibly_spontfastevents_intermediatebaseline = (possibly_spontfastevents
#                                                  & (des_df.baselinev > -60)
#                                                  & (des_df.baselinev <= -50))
# possibly_spontfastevents_highbaseline = (possibly_spontfastevents & (des_df.baselinev > -50))

# OK, from here it's I'd say that there are two types of rather fast-rise-time events - there's all these groups in the
# amp/rise-time scatters, and one of them has longer rise-time than the others and seems to stand out also in the
# rise-time/width scatter. However, with the allowable measurement noise the two groups overlap on every parameter
# (rise, width, amp and baselinev), and the dvdt plots (non-normalized and normalized) are rather confusing.
# But it does seem like the wider events occur only at specific ranges of baselinev, maybe we can find them like that:
# v1 = -53
# v2 = -48
# possibly_spontfastevents_lowbaseline = (possibly_spontfastevents & (des_df.baselinev <= v1))
# possibly_spontfastevents_intermediatebaseline = (possibly_spontfastevents
#                                                  & (des_df.baselinev > v1)
#                                                  & (des_df.baselinev <= v2))
# possibly_spontfastevents_highbaseline = (possibly_spontfastevents & (des_df.baselinev > v2))
#
# singleneuron_data.plot_depolevents(possibly_spontfastevents_lowbaseline,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_depolevents(possibly_spontfastevents_intermediatebaseline,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_depolevents(possibly_spontfastevents_highbaseline,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )

# When splitting out the events this way, by eye I'd say that the ones in the lowbaseline-group are all identical;
# in the intermediatebaseline-group there's two types, and highbaseline are another type - but the dvdt-plots don't
# corroborate that at all (especially when comparing normalized to non-normalized).
# Let's see the intermediatebaseline events in the raw data, maybe that will explain things:
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents_intermediatebaseline,
#                                      segments_overlayed=False)
# Most of the marked events are in gapFree_0000 and gapFree_0004, and then there's a whole bunch in light_wholeField_21.
# Let's see those separately:
# gapFreefile_events = des_df.file_origin.str.contains('gapFree_0000' or 'gapFree_0004')
# lightfile_events = des_df.file_origin.str.contains('light_wholeField_0021')
# singleneuron_data.plot_depolevents((possibly_spontfastevents_intermediatebaseline & gapFreefile_events),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )
# singleneuron_data.plot_depolevents((possibly_spontfastevents_intermediatebaseline & lightfile_events),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    timealignto_measure='rt20_start_idx',
#                                    prealignpoint_window_inms=3,
#                                    plotwindow_inms=13,
#                                    plot_dvdt=True,
#                                    )
# OK. The gapFree-file events (from early recording files) look like classic fast-events, and different from
# the events in the last light file. And then those two events that are in gapFree_0006 look the same as in light_21.
# So, it would seem that I'll get rid of most of the variability in waveform shapes if I just exclude the last two files (20 minutes out of >90 minutes recording)
probably_distorted_fastevents = (possibly_spontfastevents
                                 & (des_df.file_origin.str.contains('light_wholeField_0021') | des_df.file_origin.str.contains('gapFree_0006')))
probably_fastevents = (possibly_spontfastevents & ~probably_distorted_fastevents)
singleneuron_data.plot_depolevents(probably_distorted_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   timealignto_measure='rt20_start_idx',
                                   prealignpoint_window_inms=3,
                                   plotwindow_inms=13,
                                   plot_dvdt=True,
                                   )
singleneuron_data.plot_depolevents(probably_fastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   timealignto_measure='rt20_start_idx',
                                   prealignpoint_window_inms=3,
                                   plotwindow_inms=13,
                                   plot_dvdt=True,
                                   )
plt.figure(), plt.suptitle('amplitude (mV)')
des_df.loc[probably_fastevents, 'amplitude'].hist()
des_df.loc[probably_distorted_fastevents, 'amplitude'].hist()
plt.figure(), plt.suptitle('rise-time (10-90%)')
des_df.loc[probably_fastevents, 'rise_time_10_90'].hist()
des_df.loc[probably_distorted_fastevents, 'rise_time_10_90'].hist()
plt.figure(), plt.suptitle('width (50% amp)')
des_df.loc[probably_fastevents, 'width_50'].hist()
des_df.loc[probably_distorted_fastevents, 'width_50'].hist()
plt.figure(), plt.suptitle('max dvdt')
des_df.loc[probably_fastevents, 'maxdvdt'].hist()
des_df.loc[probably_distorted_fastevents, 'maxdvdt'].hist()
# %%
probably_fastevents_df = des_df[probably_fastevents]
nbins=50
probably_fastevents_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=nbins)

baselinerange = ((des_df.baselinev > -60) & (des_df.baselinev < -50))
singleneuron_data.plot_depolevents((probably_fastevents & baselinerange),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   plot_dvdt=True)
# Let's check that there isn't things in the previously filtered events that are very clearly fast-events, too;
