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
aps = des_df.event_label == 'actionpotential'
fast_events = des_df.event_label == 'fastevent'
fast_events_df = des_df[fast_events]
fast_events_df.hist(column=['rise_time_10_90', 'rise_time_20_80', 'width_50', 'amplitude'], bins=20)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True, do_normalizing=True)
singleneuron_data.plot_depolevents(fast_events, colorby_measure='baselinev', do_baselining=True)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude', cmeasure='baselinev',
                                                      fast_events=fast_events)
# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.0 to find good parameter settings. Playing with settings was done elsewhere, using saved parameters:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()

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
# %% marking 'neat' events: events occurring during a selected 5 minutes of best typical behavior
# 5 min. of recording from the first two light files: they're nice because the baselinev is held to different values

# probably_neatevents = ((des_df.file_origin == 'light_0000.abf')
#                        | ((des_df.file_origin == 'light_0001.abf')
#                           & (des_df.segment_idx <= 18))
#                        )
# adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()
# %% marking 'neat' events: the first 20 events to occur
# fastevents = des_df.event_label == 'fastevent'
# neatevents = fastevents.copy()
# neatevents[neatevents] = False
# fastevents = fastevents[fastevents]
# n = 19  # N - 1 (0-based indexing)
# i = 0
# for idx, value in fastevents.iteritems():
#     if i <= 19:
#         neatevents[idx] = True
#         i += 1
#     else:
#         break
# neatevents.name = 'n_neat_fastevents'
# adding the neatevents-series to the depolarizing_events-df:
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(neatevents)
# singleneuron_data.write_results()

# %% making manuscript figures

aps_axis, aps_dvdtaxis = singleneuron_data.plot_depolevents(((aps | fastevents) & spont_events),
                                   colorby_measure='baselinev',
                                   # color_lims=[-80, -35],
                                   prealignpoint_window_inms=7,
                                   plotwindow_inms=22)
# aps_axis.set_ylim([-5, 102])
# aps_dvdtaxis.set_xlim([-5, 102])

