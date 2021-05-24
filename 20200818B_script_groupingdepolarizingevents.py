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


# summary plots:
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

# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that light/puff-evoked things all got labeled as such
evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# There's nothing much at all of light-evoked activity, whatever did get picked up as such may as well be noise.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
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
possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 2))

plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
plt.title('spont. events, amplitude')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
plt.title('spont. events, rise-time (20-80%)')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
plt.title('spont. events, rise-time (10-90%)')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )
singleneuron_data.plot_depolevents(possibly_spontfastevents,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   )
singleneuron_data.plot_depoleventsgroups_overlayed(possibly_spontfastevents, fast_events,
                                                   group_labels=['possibly fastevents', 'fastevents'],
                                                   do_baselining=True,
                                                   do_normalizing=True
                                                   )

# Not entirely sure what to make of that, these normalized decays look to me different enough from the fast-events.



# Let's check that there isn't things in the previously filtered events that are very clearly fast-events, too;








# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
aps = des_df.event_label == 'actionpotential'
# singleneuron_data.plot_depolevents((aps & spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
# singleneuron_data.plot_depolevents((aps & ~spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='light-evoked APs')


















# %% old analysis
# notes summary:
# at first glance it's pretty clear what are the fast events - there's a few groups with amp between 9 - 12 mV,
# and another group with amp ~5mV. But then I plot them normalized and they're just not entirely identical enough...

des_df = singleneuron_data.depolarizing_events
aps = (des_df.event_label == 'actionpotential') | (des_df.event_label == 'actionpotential_on_currentpulsechange')
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'

# analysis summary figures:
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
# evoked_unlabeled_events = unlabeled_events & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )

# fast_events = des_df.event_label == 'fastevent'
# other_fast_events = des_df.event_label == 'otherfastevent'
# singleneuron_data.plot_depolevents(fast_events,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='amplitude',  # colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# singleneuron_data.plot_depolevents(other_fast_events,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='amplitude',  # colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# plt.figure()
# des_df.loc[:,'amplitude'].plot.hist(bins=30)
# plt.title('all events, amplitude')
# plt.figure()
# des_df.loc[fast_events,'amplitude'].plot.hist(bins=15)
# plt.title('fast-events, amplitude')
# plt.figure()
# des_df.loc[fast_events,'rise_time_20_80'].plot.hist(bins=15)
# plt.title('fast events, rise-time (20-80%amp)')
# plt.figure()
# des_df.loc[fast_events, 'width_50'].plot.hist(bins=15)
# plt.title('fast events, half-width')


# ongoing analysis notes:
#

# %% labeling of selected events: things that are definitely NOT fast-events
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
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


# %% quick check for any places where obvious noise-events have been detected
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_events)

# %% labeling noise-events etc.
# there's bound to be noise in the small events, and there are definitely some things that are not events but
# just the neuron being happy - but it all happens in the range of small amplitudes (1mV or so) so I don't think
# it's worth cleaning up right now.





# %% labeling of selected events: things that could be fast-events
# I looked for, but didn't find any events <1mV amp that have a waveform corresponding to the larger-amp fast-events.
#
fastevents_largerthan_params = {
                                'amplitude':1,
                                # 'baselinev':-80,
                                }
fastevents_smallerthan_params = {
                                 'rise_time_20_80': 2,
                                 }
fastevents_candidates = unlabeled_events
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)

singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='presumably all fast-events')

# %% labeling fast-events as such, and saving the data table
singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
singleneuron_data.write_results()
des_df = singleneuron_data.depolarizing_events

