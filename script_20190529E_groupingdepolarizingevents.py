import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20190529E'
singleneuron_data = SingleNeuron(neuron_name)

# notes summary:
# Thy1 mouse, lots of light pulses applied
# it's very clear that this neuron has no fast-events whatsoever, whether spontaneously or evoked;
# not even all that sure it has any real events at all so much (neuron was patched more than 6 hours after slicing).

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
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
# des_df.loc[fast_events,'amplitude'].plot.hist(bins=30)
# plt.figure()
# des_df.loc[:,'rise_time_20_80'].plot.hist(bins=30)
# des_df.loc[fast_events,'rise_time_20_80'].plot.hist(bins=30)


# ongoing analysis notes:
#

# %% labeling of selected events: things that are definitely NOT fast-events
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
singleneuron_data.plot_depolevents(aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms = 200)

# %% quick check for any places where obvious noise-events have been detected
singleneuron_data.plot_rawdatablocks(events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))

# %% labeling noise-events etc.
noiseevents_candidates = (des_df.baselinev > -35) & (des_df.amplitude < 1)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_noise=noiseevents_candidates)
singleneuron_data.plot_depolevents(noiseevents_candidates,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )





# %% labeling of selected events: things that could be fast-events
fastevents_largerthan_params = {
                                'amplitude':0.5,
                                # 'baselinev':-80,
                                }
fastevents_smallerthan_params = {
                                 'rise_time_20_80': 0.7,
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

