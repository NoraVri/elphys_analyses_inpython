# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190529A1'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Fast-events very clear by normalized waveform identicalness, grouping not so much (there just seem to be MANY groups).
# Found some fairly small ones (1 - 2mV) as well, though I'm not saying I'm sure I found ALL of those.
# Interestingly, the smallest-amp fast-events didn't seem to show up until the neuron started to depolarize,
# while during most of the recording the smaller-amp (~4-6mV) fast-events were more abundant than the larger-amp ones.
# This neuron also has many APs, with many (especially spont.ones) looking like they were evoked by a fast-event.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise
# %%
# summary plots - old:
des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'
other_events = des_df.event_label == 'other_event'  # just one of those:
aps = des_df.event_label == 'actionpotential'

# fast-events, amp and rise-time as histograms and scatters
plt.figure(), des_df.loc[fastevents,'amplitude'].plot.hist(bins=25)
plt.title('all spont. events >2mV, amplitude')
plt.figure(), des_df.loc[fastevents,'rise_time_20_80'].plot.hist(bins=25)
plt.title('all spont. events >2mV, rise-time')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      fast_events=fastevents,
                                                      )
# fast-events, baselined /baselined and normalized
singleneuron_data.plot_depolevents(fastevents,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   plt_title='fast-events')
singleneuron_data.plot_depolevents(fastevents,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='baselinev',
                                   plt_title='fast-events')

# other interesting events (if any)
singleneuron_data.plot_depolevents((aps & ~des_df.applied_ttlpulse),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='spontaneous APs')

singleneuron_data.plot_depolevents((aps & des_df.applied_ttlpulse),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='light-evoked APs')
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.2  to find good parameter settings; playing with parameters was done elsewhere somewhere (and clearly
# done with care so as to not extract too much of noisy things in the <1mV amp range);
# using saved parameter settings to re-create depolarizing-events data table:
# singleneuron_data.get_depolarizingevents_fromrawdata()


# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events
# fastevents = des_df.event_label == 'fastevent'

# 1. seeing that evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# I saw one or two light-responses where something that looked like a subthreshold depolarizing event didn't
# get picked up as evoked, even though by eye we might say it is (because it's riding an after-potential of an evoked response).
# It doesn't look like such occurrences should pose any problems for analyses, so leaving it as is.
# Evoked responses look mostly like compound synaptic depolarizations and spikelets.

# 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')

# notes:
# Looks good as far as extracting events; tons of things going on in there, it'll be quite a job to
# separate out classic fast-events only (caught some doublets by eye, that's gonna be interesting...).
# Let's start by getting rid of things that are just gonna be distracting:
# In the first recording file (gapFree_0000) it seems that the neuron is not actually so well patched initially
# (very high apparent 'Rin') but by about 471s into the recording it's looking good and stable.
# Labeling all events that happen before that as 'noise':
# sr = float(singleneuron_data.blocks[0].segments[0].analogsignals[0].sampling_rate)
# trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices']['gapFree_0000.abf']['t_start']
# noise_end_idx = (471 - trace_start_t) * sr
# noisy_events = (des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx < noise_end_idx)
# singleneuron_data.depolarizing_events.loc[noisy_events, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()

# Let's see amplitude and rise-time histograms and scatter for the events we're left with:
# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('all unlabeled spont. events, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('all unlabeled spont. events, rise-time (20-80%)')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
# plt.title('all unlabeled spont. events, rise-time (10-90%)')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# It is evident both from the histograms and the scatter that there are multiple groups of events.
# For starters, there's a clear break in the amplitude histogram at 3mV; let's see events with amp > 3 first:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 3))
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True
#                                    )
# these all look like classic fast-events, except the one that's larger than all the others (~12 mV, fast-events <10)
# has a clearly compound upslope and higher baselinev.
# Let's see where it is:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(possibly_spontfastevents & (des_df.amplitude > 12)))
# very much towards the end of recordings, cell clearly not happy anymore, this is the last large-amp event it fires.
# Labeling it as "other_event":
# other_event = (possibly_spontfastevents & (des_df.amplitude > 12))
# singleneuron_data.depolarizing_events.loc[other_event, 'event_label'] = 'other_event'
# singleneuron_data.write_results()
# correction: this single 'other event' is in fact clearly a compound event as we've (by now) seen in many other
# neurons; labeling it as such:
# compound_event = (singleneuron_data.depolarizing_events.event_label == 'other_event')
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# The events > 3mV we're left with are definitely all fast-events: normalized decay shape practically identical,
# except for some change with different baselineV. The events are between 3.5 and 9.5mV, and may be in 8 or 9 groups,
# with the smallest amplitudes being most abundant.
# Labeling them as fastevents:
# fastevents = (possibly_spontfastevents & (des_df.amplitude > 3))
# singleneuron_data.depolarizing_events.loc[fastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Now let's see if we can easily find more fast-events in the events with amp < 3mV: -
# There's a couple of events amp 1.5 - 2.5mV that look like they could be fast-events; most of them seem to occur at
# fairly depolarized baselineV, and from the rise-time histograms and the scatter it looks like it may be possible to
# narrow down criteria a bit further and find them.
# Let's keep narrowing down on events by selecting by rise-time, starting with 2ms (based on histogram):
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_10_90 < 2))
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 < 0.8))
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.rise_time_20_80 > 0.3)) # the one that has shorter rise-time than that is a double-event
# Giving up on finding events < 1mV, but I'm still pretty sure there's some fast-events of 1-2mV to find:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 1))
# singleneuron_data.plot_depoleventsgroups_overlayed(fastevents, possibly_spontfastevents,
#                                                    group_labels=['fastevents', 'unlabeled events'],
#                                                    plotwindow_inms = 15,
#                                                    do_baselining=True,
#                                                    # do_normalizing=True
#                                                    )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms = 15,
#                                    do_baselining=True,
#                                    # do_normalizing=True
#                                    )
# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('all unlabeled spont. events, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('all unlabeled spont. events, rise-time (20-80%)')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
# plt.title('all unlabeled spont. events, rise-time (10-90%)')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# The events we're left with all look identical to each other, and their rise is identical to fastevents
# but their decay is a bit faster. Let's see if it still makes sense (also considering baselinev):
# singleneuron_data.plot_depolevents((fastevents | possibly_spontfastevents),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    do_normalizing=True)
# yes it does - all these small ones occur at depolarized baselineV, and follow the expected decay-shape change.
# Labeling them as fast-events:
# singleneuron_data.depolarizing_events.loc[possibly_spontfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
# aps = des_df.event_label == 'actionpotential'
# spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
# singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
# singleneuron_data.plot_depolevents((aps & ~des_df.applied_ttlpulse),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
#
# singleneuron_data.plot_depolevents((aps & des_df.applied_ttlpulse),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='light-evoked APs')
# interestingly, the spont. and light-evoked APs look VERY similar - there just seem to be more in the spont. group.
# spont.APs often seem to have a 'foot' made by a fast-event, will be interesting to look into.

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% selecting 5 minutes of best typical behavior and marking 'neat' events
# For this neuron, the light files are the neatest (until the neuron suddenly depolarizes and dies) - there's exactly
# 5 minutes of consecutive neat recording time in those files.
# probably_neatevents = ((des_df.file_origin == 'light_0000.abf')
#                        | (des_df.file_origin == 'light_0001.abf')
#                        | ((des_df.file_origin == 'light_0002.abf') & (des_df.segment_idx <= 13))
#                        )
# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()