# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20190401B1'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:



# summary plots:



# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# overall a quite nice and stable-looking recording (no -DC applied anywhere to keep baselinev) except towards
# the very end (shortPulse 01) where baselinev deteriorates badly. Also, it seems like fast-events frequency is
# going down over time, disappearing to almost 0 after about 45 minutes of recording.

# I will use gapFree_0000 for extracting depolarizing events, as this is the trace with the most fast-events in it.
# the neuron's oscillations are nicely captured by a 10Hz lp-filter; AHP width window increased to 200ms because 150ms
# often cuts it too close; min_depolspeed increased to 0.2mV/ms because below that there's really just noise (from seeing the event-detect-trace derivative).

# block_no = 0
# segment_no = 0
# time_slice = [400, 500]  # [800, 950]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
#                                                     min_depolamp=0.1,
#                                                     oscfilter_lpfreq=10,
#                                                     ahp_width_window=200,
#                                                     min_depolspeed=0.2,
#
# )

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=0.1,
#                                                      min_depolspeed=0.2,
#                                                      ahp_width_window=200,
#                                                      oscfilter_lpfreq=10)
# singleneuron_data.write_results()


# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=3)
# singleneuron_data.write_results()

# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# 1. seeing that light/puff-evoked things all got labeled as such
# notes:
# no ttl-evoked events recorded in this experiment.

# 2. seeing that spontaneous fast-events got picked up
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# singleneuron_data.plot_rawdatablocks(events_to_mark=possibly_spontfastevents, segments_overlayed=False)
# notes:


# plotting events parameters:
possibly_spontfastevents_df = des_df[unlabeled_spont_events]
possibly_spontfastevents_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=unlabeled_spont_events,
                                                      )
