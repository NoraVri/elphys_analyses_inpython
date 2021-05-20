# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

neuron_name = ''
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# This neuron definitely has fast-events, though only 8 of them altogether
# and amplitude groups are not very clear (normalized decay identicalness is very nice though).
# This neuron also has other_fastevents (3 events, 2 amplitudes) and other events that I have no idea what they are.

# summary plots:

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:

singleneuron_data.get_depolarizingevents_fromrawdata()


# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that evoked things all got labeled as such
evoked_events = des_df.applied_ttlpulse
singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, time_axis_unit='s')
# notes:

# Let's filter down to things with amp > 2mV, and see amplitude and rise-time for the rest to narrow down from there:
possibly_spontfastevents = (possibly_spontfastevents & (des_df.amplitude > 2))
plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
plt.title('all spont. events >2mV, amplitude')
plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
plt.title('all spont. events >2mV, rise-time')
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=possibly_spontfastevents,
                                                      )





# Let's check that there isn't things in the events <2mV that are very clearly fast-events, too;








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







# %% labeling of selected events: compound conditions
fastevents_largerthan_params = {
                                'amplitude': 0.5,
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
