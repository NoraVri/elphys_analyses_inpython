import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20190529B'
singleneuron_data = SingleNeuron(neuron_name)
# %%
# notes summary:
# this neuron does not have any spontaneous fast-events of any kind (only tons of tiny spikelets);
# its evoked events are worth taking a closer look at though, as at first look they behave rather
# like fast-events would

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'

# analysis summary figures:
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
evoked_unlabeled_events = unlabeled_events & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events
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
# interestingly, the majority of light-evoked APs has no shoulder, and seem to behave mostly like fast-events
# (identical normalized decay except for decay slowing down for more depolarized baselinev; and then there's this
# one group of events that for some reason has a particularly fast decay).
# Also, almost all these APs seem to be evoked by rather high amplitude, wide pre-potentials, and the baseline-points
# are not always so well found by the algorithm.


# %% quick check for any places where obvious noise-events have been detected
# singleneuron_data.plot_rawdatablocks(events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))
#
# # there's exactly one sweep during which the neuron oscillates (and doesn't do anything else)
# # and osc.upslopes are picked up as 'events'... labeling all these as noise-events:
# oscupslope_events = des_df.file_origin == 'light_0000.abf'
# singleneuron_data.depolarizing_events.loc[oscupslope_events, 'event_label'] = 'noiseevent'
#
# # and in gapFree_0000, there's a weird noise-thing that got picked up as three events (that are rather big;
# # they are the only three events between 351 - 351.05 s in the trace [but account also for the 18s cut off trace start])
# # removing these, too:
# sampling_rate = float(singleneuron_data.blocks[0].segments[0].analogsignals[0].sampling_rate)  # in Hz
# noise_startidx = (351 - 18) * sampling_rate
# noise_endidx = (351.05 - 18) * sampling_rate
# noiseevents_byeye = ((des_df.file_origin == 'gapFree_0000.abf')
#                      & (des_df.peakv_idx > noise_startidx) & (des_df.peakv_idx < noise_endidx))
# singleneuron_data.depolarizing_events.loc[noiseevents_byeye, 'event_label'] = 'noiseevent'
#
# # all other events look good, or they're too small and insignificant for this investigation for me to
# # cut them all out now
# singleneuron_data.write_results()



# %% labeling of selected events: things that could be fast-events
fastevents_largerthan_params = {
                                'amplitude':1,
                                # 'baselinev':-80,
                                }
fastevents_smallerthan_params = {
                                 # 'rise_time_20_80': 0.7,
                                 }
fastevents_candidates = (unlabeled_events & ~des_df.applied_ttlpulse)
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)

singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='presumably all fast-events')

# this neuron has nothing in its spontaneous activity that looks like fast-events.
