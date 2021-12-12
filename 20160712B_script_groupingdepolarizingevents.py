# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20160712B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:







# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# neuron kicks into very steeply wacky oscillations towards the very end (after ~1hr of recording) some of which are
# probably gonna get picked up as 'events' by the algorithm. Other than that though the oscs are very steady in
# freq (~8mV), a little less so in amp, though it's generally between 3 - 8 mV. AHPs are 100-120ms max.

# block_no = 0
# segment_no = 0
# time_slice = [100, 250]
#
# (eventmeasures_dict,
#  depolevents_readingnotes_dict) = singleneuron_data.plot_eventdetecttraces_forsegment(block_no, segment_no,
#                                                                                       return_dicts=True,
#                                                                                       time_slice=time_slice,
# # check that AHP width window wide enough
# )
# extraction with default settings looks quite good; we don't need all the very small events, so I'll just skip those for now.

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=1.5)
# singleneuron_data.write_results()

# %%
# %% plots and analyses: seeing and labeling depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100

# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_spont_events, segments_overlayed=False)
# notes:

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting all as-yet unlabeled events parameters:
des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )

# Labeling fast-events and other events fitting in categories not labeled automatically (fastevent, compound_event, other_event, noiseevent)
# 1.

# events_underinvestigation = (unlabeled_spont_events & (des_df.))
# singleneuron_data.plot_depolevents(events_underinvestigation,
#                                    colorby_measure='baselinev',
#                                    plotwindow_inms=15,
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    plot_dvdt=True
#                                    )
# des_df[events_underinvestigation].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
#                                  bins=nbins,
#                                  )
# plt.suptitle('events currently under investigation')