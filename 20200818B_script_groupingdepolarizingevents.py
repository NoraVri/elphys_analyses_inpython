# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20200818B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# quite alright recording overall, although neuron stops displaying spont.events at some point and baselineV
# deteriorating a bit throughout; also evoked APs clearly deteriorate towards the end (no spont. or light-evoked seen
# anywhere in the recording).

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

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.0 to find good parameter settings. Playing with settings was done elsewhere, using saved parameters:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_evokedbylight #aps_spont # aps_oncurrentpulsechange
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# aps_oncurrentpulsechange: not all of these are all that neat - towards the end of recording evoked APs are clearly
# degenerate, and there are some that didn't reach above 0mV and therefore didn't get labeled AP. Still, looks OK enough.
# no spont. or light-evoked APs recorded.
# %% plots and analyses: seeing and labeling depolarizing events
# des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# There's nothing much at all of light-evoked activity, whatever did get picked up as such may as well be noise.

# 2. seeing that spontaneous fast-events got picked up
# spont_events = ~des_df.applied_ttlpulse
# unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
# possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:
# As usual tons of tiny things but definitely all the clear events (3-4mV and up in this neuron)
# got picked up. My eye caught at least one currentpulsechange that didn't get labeled properly, but other than that
# it looks OK.

# Let's see amplitude and rise-time and narrow down from there:
# In the amp histogram there's a clear break at 3mV, but in the amp/rise-time scatter the only group of points
# that would clearly indicate fast-events (large-amp and small rise-time) has amp > 8mV.
# Let's see these largest events first, and then add in smaller ones later:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 8))
# Yea those are fast-events alright, perfectly identical normalized decay waveforms even if amplitude grouping
# not very clear (could be anywhere between 5 - 8 groups, events have amps between 9 and 12mV).
# Labeling them as such:
# singleneuron_data.depolarizing_events.loc[possibly_spontfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# Now let's see what we're left with, and further narrow down criteria:
# I'm pretty sure I'm now seeing some of those currentpulsechanges that didn't get picked up right; they are
# quite recognizable by their very slow rise yet pretty big amp. Let's see:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(possibly_spontfastevents
#                                                      & (des_df.rise_time_10_90 > 2.5)
#                                                      & (des_df.amplitude > 2)))
# Indeed. Labeling them as such:
# currentpulsechanges = (possibly_spontfastevents & (des_df.rise_time_10_90 > 2.5) & (des_df.amplitude > 2))
# singleneuron_data.depolarizing_events.loc[currentpulsechanges, 'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()

# By now we're left with only 4 events, the rest all being very small and slow (<2mV >2ms).
# Let's see the four that are >2mV; by eye it looks like two are spikelets and two are fast-events:
# possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 2))

# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('spont. events, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (20-80%)')
# plt.figure(), des_df.loc[possibly_spontfastevents,'maxdvdt'].plot.hist(bins=60)
# plt.title('spont. events, maxdvdt')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )
# singleneuron_data.plot_depolevents(possibly_spontfastevents,
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    )
# singleneuron_data.plot_depoleventsgroups_overlayed(possibly_spontfastevents, fast_events,
#                                                    group_labels=['possibly fastevents', 'fastevents'],
#                                                    do_baselining=True,
#                                                    do_normalizing=True
#                                                    )
# OK yea those are all fastevents; they just look noisier because they're smaller than the rest of the events that got
# labeled so far. Labeling them as such:
# singleneuron_data.depolarizing_events.loc[possibly_spontfastevents, 'event_label'] = 'fastevent'
# singleneuron_data.write_results()

# I further examined the remaining events, and I believe they are all small, slow events: I looked specifically at
# events with relatively high maxdvdt values, but by parameter values there isn't a separation anywhere and also from
# the line plots it's impossible to tell for any of the remaining events whether it would really be a fastevent or not.
#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% marking 'neat' events: events occurring during stable and 'good-looking' periods of recording
# plotting raw data with events marked:
# singleneuron_data.plot_rawdatablocks(events_to_mark=(fastevents | (aps & spont_events)),
#                                      segments_overlayed=False)
# notes:
# neuron doesn't have any spont.APs so it's a bit hard to tell where recording goes 'bad'; baselineV is very slowly
# deteriorating throughout recordings. But there is a point in light#2 where neuron becomes visibly more leaky; it also
# stops firing much of spont.fastevents after this point. So I'll mark the first three recording files as 'neat':
# neat_events = des_df.file_origin.str.contains(pat=('gapFree_000|light_0000|light_0001'))
# neat_events.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neat_events)
# singleneuron_data.write_results()