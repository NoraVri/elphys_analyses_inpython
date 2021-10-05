# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190729A'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
# Over two hours of recording, and nothing interesting happening at all.
# Events in this neuron are all 2mV or smaller, and in the amp/rise-time distributions there is nothing to
# indicate that there would be a distinct group of fast-events.

des_df = singleneuron_data.depolarizing_events
fastevents = des_df.event_label == 'fastevent'  # see plots and analyses section...
compound_events = des_df.event_label == 'compound_event'  # see plots and analyses section...
aps = des_df.event_label == 'actionpotential'
spont_events = ~des_df.applied_ttlpulse  #
unlabeled_events = des_df.event_label.isna()  # all events that were not given a label
unlabeled_spontevents = (spont_events & unlabeled_events)
smallslowevents = unlabeled_spontevents  # unless seen otherwise



# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# used block no.1 to find good parameter settings, time-sliced 180-280; playing with settings was done elsewhere,
# using stored parameter settings to get data table (since it's such a long recording it takes a long time to run this:
# singleneuron_data.get_depolarizingevents_fromrawdata()
# singleneuron_data.write_results()


# %% plots: seeing that depolarizing events got extracted nicely
des_df = singleneuron_data.depolarizing_events

# 1. seeing that evoked things all got labeled as such
# notes: no light-evoked events in this neuron (though it as AP5 + DNQX applied for some of the time)


# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
possibly_spontfastevents = (spont_events & unlabeled_events)
# notes:
# events are all <1.25mV except for one that registers as 12mV with rise-time > 3ms.
# Let's see what's that one:
# singleneuron_data.plot_depolevents((possibly_spontfastevents & (des_df.amplitude > 10)))
# that's a currentpulsechange that escaped the algorithm - labeling it as such:
# singleneuron_data.depolarizing_events.loc[(possibly_spontfastevents & (des_df.amplitude > 10)),
#                                           'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()

# Let's see amplitude and rise-time to narrow down from there:
# plt.figure(), des_df.loc[possibly_spontfastevents,'amplitude'].plot.hist(bins=60) # 60bins to start with
# plt.title('spont. events, amplitude')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_20_80'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (20-80%)')
# plt.figure(), des_df.loc[possibly_spontfastevents,'rise_time_10_90'].plot.hist(bins=60)
# plt.title('spont. events, rise-time (10-90%)')
# singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
#                                                       cmeasure='baselinev',
#                                                       spont_subthreshold_depols=possibly_spontfastevents,
#                                                       )

# I see nothing in any of these plots that would indicate there are fast-events. Events are all very small (<2mV)
# and rise-time vs amp scatter just shows a cloud.

# 3. seeing that all things that got labeled as 'actionpotential' automatically are indeed that
# aps = des_df.event_label == 'actionpotential'
# singleneuron_data.plot_depolevents((aps & spont_events),
#                                    do_baselining=True,
#                                    colorby_measure='baselinev',
#                                    prealignpoint_window_inms=30,
#                                    plotwindow_inms = 100,
#                                    plt_title='spontaneous APs')
# Looks OK, they all seem to be evoked by current

#### -- this concludes sorting through all sub-threshold events and labeling them -- ####
# %% selecting 5 minutes of best typical behavior and marking 'neat' events
# this neuron has no fast-events, so the first 5 minutes of the first recording file will do just fine.
# block_name = 'gapFree_0000.abf'
# window_start_t = 0
# window_end_t = 300
# sampling_frequency = singleneuron_data.blocks[0].channel_indexes[0].analogsignals[0].sampling_rate
# trace_start_t = 0
# neat5min_start_idx = (window_start_t - trace_start_t) * float(sampling_frequency)
# neat5min_end_idx = (window_end_t - trace_start_t) * float(sampling_frequency)
# probably_neatevents = ((des_df.file_origin == block_name)
#                        & (des_df.peakv_idx >= neat5min_start_idx)
#                        & (des_df.peakv_idx < neat5min_end_idx)
#                        )
# # adding the neatevents-series to the depolarizing_events-df:
# probably_neatevents.name = 'neat_event'
# singleneuron_data.depolarizing_events = singleneuron_data.depolarizing_events.join(probably_neatevents)
# singleneuron_data.write_results()
# %%

